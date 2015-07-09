package org.elasticsearch.river.cassandra;

import java.util.Map;

public class CassandraCFData {
	public String start;
	public Map<String, Map<String, byte[]>> rowColumnMap;
}
