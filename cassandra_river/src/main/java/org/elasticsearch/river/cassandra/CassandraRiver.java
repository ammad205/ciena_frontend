package org.elasticsearch.river.cassandra;

import static org.elasticsearch.client.Requests.indexRequest;

import java.util.UUID;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadFactory;

import org.elasticsearch.action.bulk.BulkRequestBuilder;
import org.elasticsearch.client.Client;
//import org.elasticsearch.common.UUID;
import org.elasticsearch.common.inject.Inject;
import org.elasticsearch.common.util.concurrent.ThreadFactoryBuilder;
import org.elasticsearch.common.xcontent.support.XContentMapValues;
import org.elasticsearch.river.AbstractRiverComponent;
import org.elasticsearch.river.River;
import org.elasticsearch.river.RiverName;
import org.elasticsearch.river.RiverSettings;
import org.elasticsearch.script.ScriptService;
import static org.elasticsearch.common.xcontent.XContentFactory.*;
import org.elasticsearch.common.xcontent.XContentBuilder;
import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;

public class CassandraRiver extends AbstractRiverComponent implements River {

	private final Client client;

	private ExecutorService threadExecutor;
	private volatile boolean closed;

	// Cassandra settings
	private final String hosts;
	private final String username;
	private final String password;

	private final String clusterName;
	private final String keyspace;
	private final String columnFamily;
	private final int batchSize;

	// Index settings
	private final String typeName;
	private final String indexName;
	static final String DEFAULT_UNIQUE_KEY = "id";

	@Inject
	protected CassandraRiver(RiverName riverName, RiverSettings riverSettings,
			Client client, ScriptService scriptService) {
		super(riverName, riverSettings);
		this.client = client;

		if (riverSettings.settings().containsKey("cassandra")) {
			@SuppressWarnings("unchecked")
			Map<String, Object> couchSettings = (Map<String, Object>) settings
					.settings().get("cassandra");
			this.clusterName = XContentMapValues.nodeStringValue(
					couchSettings.get("cluster_name"), "DEFAULT_CLUSTER");
			this.keyspace = XContentMapValues.nodeStringValue(
					couchSettings.get("keyspace"), "DEFAULT_KS");
			this.columnFamily = XContentMapValues.nodeStringValue(
					couchSettings.get("column_family"), "DEFAULT_CF");
			this.batchSize = XContentMapValues.nodeIntegerValue(
					couchSettings.get("batch_size"), 1000);
			this.hosts = XContentMapValues.nodeStringValue(
					couchSettings.get("hosts"), "host1:9161,host2:9161");
			this.username = XContentMapValues.nodeStringValue(
					couchSettings.get("username"), "USERNAME");
			this.password = XContentMapValues.nodeStringValue(
					couchSettings.get("password"), "P$$WD");
		} else {
			/*
			 * Set default values
			 */
			this.clusterName = "DEFAULT_CLUSTER";
			this.keyspace = "DEFAULT_KS";
			this.columnFamily = "DEFAULT_CF";
			// this.batchSize = 1000;
			this.batchSize = 3;
			this.hosts = "host1:9161,host2:9161";
			this.username = "USERNAME";
			this.password = "P$$WD";
		}

		if (riverSettings.settings().containsKey("index")) {
			@SuppressWarnings("unchecked")
			Map<String, Object> couchSettings = (Map<String, Object>) settings
					.settings().get("index");
			this.indexName = XContentMapValues.nodeStringValue(
					couchSettings.get("index"), "DEFAULT_INDEX_NAME");
			this.typeName = XContentMapValues.nodeStringValue(
					couchSettings.get("type"), "DEFAULT_TYPE_NAME");

		} else {
			this.indexName = "DEFAULT_INDEX_NAME";
			this.typeName = "DEFAULT_TYPE_NAME";
		}
	}

	@Override
	public void start() {
		ThreadFactory daemonThreadFactory = new ThreadFactoryBuilder()
				.setNameFormat("Queue-Indexer-thread-%d").setDaemon(false)
				.build();
		threadExecutor = Executors.newFixedThreadPool(1, daemonThreadFactory);

		logger.info("Starting cassandra river");
		/* gets the db instance for the corresponding keyspace */
		CassandraDB db = CassandraDB.getInstance(this.hosts, this.username,
				this.password, this.clusterName, this.keyspace);
		String start = "";
		// this.batchSize = 3;
		/* INFINITE LOOP */
		while (true) {
			if (closed) {
				return;
			}
			/* asks the db instance to get the data from cassandra */
			/*
			 * the 1000 specifies the maximum number of data to get in a single
			 * go
			 */
			CassandraCFData cassandraData = db.getCFData(columnFamily, start,
					1000);
			/* checks if any new data was found in the database */
			if (start != cassandraData.start) {
				start = cassandraData.start;
				threadExecutor.execute(new Indexer(this.batchSize,
						this.typeName, this.indexName, cassandraData));
			}
		}
	}

	@Override
	public void close() {
		if (closed) {
			return;
		}
		logger.info("closing cassandra river");
		closed = true;
		threadExecutor.shutdownNow();
	}

	private class Indexer implements Runnable {
		// private final int batchSize;
		private int batchSize; // fixme for verifying only
		private final CassandraCFData keys;
		private final String typeName;
		private final String indexName;

		public Indexer(int batchSize, String typeName, String indexName,
				CassandraCFData keys) {
			this.batchSize = batchSize;
			this.typeName = typeName;
			this.indexName = indexName;
			this.keys = keys;
		}

		@Override
		public void run() {
			if (keys == null || keys.rowColumnMap == null) {
				logger.info("keys are null in indexer thread" + keys);
				return;
			}
			logger.info("Starting thread with {} keys",
					this.keys.rowColumnMap.size());
			if (closed) {
				return;
			}

			BulkRequestBuilder bulk = client.prepareBulk();
			logger.info("Current bulk size: {}", bulk.numberOfActions());
			logger.info("Total batch size set: {}", this.batchSize);
			Map<String, byte[]> columns;
			for (String key : this.keys.rowColumnMap.keySet()) {
				logger.info("Current key: {}", key);
				try {
					// String id =
					// UUID.nameUUIDFromBytes(key.getBytes()).toString();
					String id = UUID.randomUUID().toString();
					// String id = key.toString();
					// FIXME
					// bulk.add(indexRequest(this.indexName).type(this.typeName).id(id).source(this.keys.rowColumnMap.get(key)));
					//columns = this.keys.rowColumnMap.get(key);
					// bulk =
					//bulk.add(indexRequest(this.indexName).type(this.typeName)
						//	.id(id).source(buildJson(columns)));

					bulk.add(client.prepareIndex(this.indexName,
							this.typeName).setSource(buildJson(this.keys.rowColumnMap.get(key))));

					logger.info("Current bulk size: {}", bulk.numberOfActions());
					logger.info("Total batch size set: {}", this.batchSize);

				} catch (Exception e) {
					logger.error("failed to entry to bulk indexing");
				}

				/* data insertion condition for elasticsearch */
				if (bulk.numberOfActions() >= this.batchSize
						|| bulk.numberOfActions() == keys.rowColumnMap.size()) {
					logger.info("*********** Inserting data into elasticsearch **********");
					saveToEs(bulk);
					bulk = client.prepareBulk();
					logger.info("*********** Data inserted into elasticsearch **********");
					// logger.info("*********** Closing thread **************");
					// close();
					// FIXME the above and below line was added for test purpose
					// only
					// this.batchSize = 1000;
				}
			} // end of for loop
		}

		private XContentBuilder buildJson(Map<String, byte[]> columns) {
			try {
				XContentBuilder builder = jsonBuilder().startObject();
				for (String key : columns.keySet()) {
					if (DataConverter.intColumns.contains(key)) {
						BigInteger value = DataConverter.getIntValue(columns
								.get(key));
						builder = builder.field(key, value.longValue());
					} else if (DataConverter.strColumns.contains(key)) {
						builder = builder.field(key,
								DataConverter.getStringValue(columns.get(key)));
					} else if (key.equals("destip") || key.equals("sourceip")) {
						long value = DataConverter.getLongValue(columns
								.get(key));
						builder = builder.field(key,
								DataConverter.longToIp(value));
					} else if (key.equals("teardown_time")
							|| key.equals("setup_time")) {
						long epoch = DataConverter
								.getIntValue(columns.get(key)).longValue();
						String date = new java.text.SimpleDateFormat(
								"yyyy-MM-dd HH:mm:ss")
								.format(new java.util.Date(epoch / 1000));
						builder = builder.field(key,
								date.replace(" ", "T"));
					} else if (key.equals("protocol")) {
						BigInteger value = DataConverter.getIntValue(columns
								.get(key));
						String valueStr = DataConverter.applyIntMapping(key,
								value);
						builder = builder.field(key, valueStr);
					} else {
						builder = builder.field(key, "");
					}
				}
				builder = builder.endObject();
				return builder;
			} catch (Exception e) {
				return null;
			}
		}

		/*
		 * Persists data to elastic search
		 */
		private boolean saveToEs(BulkRequestBuilder bulk) {
			logger.info("Inserting {} keys in ES", bulk.numberOfActions());

			try {
				bulk.execute().addListener(new Runnable() {
					@Override
					public void run() {
						logger.info("Processing done!");
					}
				});
			} catch (Exception e) {
				logger.error("failed to execute bulk", e);
				return false;
			}

			return true;
		}
	}
}
