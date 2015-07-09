import java.util.*;
import java.nio.ByteBuffer;

import me.prettyprint.cassandra.model.AllOneConsistencyLevelPolicy;
import me.prettyprint.cassandra.serializers.StringSerializer;
import me.prettyprint.cassandra.serializers.BytesArraySerializer;
import me.prettyprint.cassandra.service.CassandraHostConfigurator;
import me.prettyprint.cassandra.service.FailoverPolicy;
import me.prettyprint.hector.api.Cluster;
import me.prettyprint.hector.api.Keyspace;
import me.prettyprint.hector.api.beans.ColumnSlice;
import me.prettyprint.hector.api.beans.HColumn;
import me.prettyprint.hector.api.beans.OrderedRows;
import me.prettyprint.hector.api.beans.Row;
import me.prettyprint.hector.api.factory.HFactory;
import me.prettyprint.hector.api.query.RangeSlicesQuery;

/*
 * CLASS: CassandraDB
 * the class which handles all the cassandra
 * database related tasks for extracting data
 */
public class CassandraDB {
	private static final StringSerializer STR = StringSerializer.get();
	public static final String COMPOSITE_SEPARATOR = "~";

	private Cluster cluster;
	private Keyspace keyspace;
	private int batchSize;

	private static HashMap<String, CassandraDB> instances = new HashMap<String, CassandraDB>();

	private CassandraDB(String hosts, String username, String password,
			String clustername, String keyspace) {
		init(clustername, hosts, username, password, keyspace);
	} // end of constructor

	protected void init(String clustername, String hosts, String username,
			String password, String keyspace) {
		CassandraHostConfigurator hostconfig = new CassandraHostConfigurator(
				hosts);
		hostconfig.setRetryDownedHosts(true);
		hostconfig.setRetryDownedHostsDelayInSeconds(5);
		hostconfig.setRetryDownedHostsQueueSize(-1); // no bounds
		this.cluster = HFactory.getOrCreateCluster(clustername, hostconfig);

		Map<String, String> credentials = new HashMap<String, String>();
		if (username != null && username.length() > 0) {
			credentials.put("username", username);
			credentials.put("password", password);
		}

		this.keyspace = HFactory.createKeyspace(keyspace, cluster,
				new AllOneConsistencyLevelPolicy(),
				FailoverPolicy.ON_FAIL_TRY_ALL_AVAILABLE);
	} // end of function

	public static CassandraDB getInstance(String hosts, String username,
			String password, String clustername, String keyspace) {
		String instanceKey = clustername + "|" + keyspace; // TODO A cleaner key
															// would be nice
		CassandraDB instance = null;

		synchronized (CassandraDB.class) {
			instance = instances.get(instanceKey); // gets the instance
													// corresponding to a
													// instancekey (static
			if (instance == null) {
				instance = new CassandraDB(hosts, username, password,
						clustername, keyspace); // creates a object and calls
												// the init method
				instances.put(instanceKey, instance);
			}
		}

		return instance;
	} // end of function

	public int getBatchSize() {
		return batchSize;
	} // end of function

	public void setBatchSize(int batchSize) {
		this.batchSize = batchSize;
	}

	/*
	 * the method which extracts data from the database with limit specified by
	 * the limit variable
	 */
	public CassandraCFData getCFData(String columnFamily, String start,
			int limit) {
		int columnLimit = 100;
		CassandraCFData data = new CassandraCFData(); // object for data storage
		String lastEnd = null;

		/* for storing data while extracting it */
		Map<String, Map<String, byte[]>> cfData = new HashMap<String, Map<String, byte[]>>();
		/* returns key, name, value in this interface <K,N,V> */
		RangeSlicesQuery<String, String, byte[]> query = HFactory
				.createRangeSlicesQuery(keyspace, STR, STR,
						BytesArraySerializer.get());
		/* SETTING the query parameters */
		query.setColumnFamily(columnFamily);
		query.setKeys(start, "");
		query.setRange("", "", false, columnLimit);
		query.setRowCount(limit);
		// FIXME with logger
		System.out.println("************* executing query *************");
		OrderedRows<String, String, byte[]> rows = query.execute().get();
		System.out.println("************* query executed *************");
		System.out.println("*************" + rows.getCount()
				+ " rows found *************");
		/* checks if any data was found */
		System.out.println("start = " + start);
		if (rows.getCount() != 1) {
			if (rows.peekLast() == null) {
				System.out.println("************* rows.peekLast() is null");
				// data.start = null;
				data.start = start; // testing condition may fix the problem
				return data;
			} // added to avoid the null exception
				// FIXME
			System.out.println("peek last key " + rows.peekLast().getKey());
			/* setting the value of the start variable for future range queries */
			lastEnd = rows.peekLast().getKey();
			data.start = lastEnd;
		} else {
			// data.start = null;
			data.start = start; // testing condition may fix the problem
			return data;
		}

		/* arranging the map */
		for (Row<String, String, byte[]> row : rows.getList()) {
			Map<String, byte[]> columnMap = new HashMap<String, byte[]>();
			ColumnSlice<String, byte[]> columnData = row.getColumnSlice();
			for (HColumn<String, byte[]> column : columnData.getColumns()) {
				try {
					//String strValue = DataConverter.convertData(column.getName(), column.getValue());
					//if (strValue != "") {
						columnMap.put(column.getName(), column.getValue());
					//}
					// FIXME
					System.out.println(column.getName() + " = " + column.getValue());
				} catch (Exception e) {
					System.out.println("Error: " + column.getName() + "  " + e);
				}
				// FIXME temp pause added
				try {
					Thread.sleep(100);
				} catch (InterruptedException ex) {
					Thread.currentThread().interrupt();
				}

			} // end of inner loop

			cfData.put(row.getKey(), columnMap);
		} // end of outer loop

		data.rowColumnMap = cfData;
		return data;
	}
}
