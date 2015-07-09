import java.util.Date;

public class MainClass {

	public static void main(String[] args) {
		
		CassandraDB db = CassandraDB.getInstance("117.20.30.70:9160", "Cassandra", "Cassandra", "Contrail", "ContrailAnalytics");
	
		CassandraCFData cassandraData = db.getCFData("FlowRecordTable", "", 1000);		
	}
}
