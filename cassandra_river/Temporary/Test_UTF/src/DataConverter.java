import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/*
 * CLASS: DataConverter
 * The class which contains all the data
 * converters used for converting the extracted 
 * analytics data from the cassandra db
 */
public class DataConverter {

	private final static List<String> strColumns = Arrays.asList(
			"input_interface", "vrouter", "data_sample", "output_interface",
			"reverse_uuid", "vm", "sourcevn", "action", "destvn");

	private final static List<String> intColumns = Arrays.asList("mpls_label",
			"tcp_flags", "stddev_interarrival", "tos", "mean_interarrival",
			"max_interarrival", "min_interarrival", "bytes", "packets",
			"direction_ing", "protocol", "sport", "dport");

	private static final LinkedHashMap<String, Long> protoToNum = new LinkedHashMap<String, Long>();

	static {
		protoToNum.put("ip", Long.valueOf(0));
		protoToNum.put("icmp", Long.valueOf(1));
		protoToNum.put("ggp", Long.valueOf(3));
		protoToNum.put("tcp", Long.valueOf(6));
		protoToNum.put("egp", Long.valueOf(8));
		protoToNum.put("pup", Long.valueOf(12));
		protoToNum.put("udp", Long.valueOf(17));
		protoToNum.put("hmp", Long.valueOf(12));
		protoToNum.put("xns-idp", Long.valueOf(22));
		protoToNum.put("rdp", Long.valueOf(27));
		protoToNum.put("rvd", Long.valueOf(66));
	}

	/*
	 * FUNCTION: convertData(key,rawDara) It takes data in the form of bytes and
	 * returns its string form. It converts the data based on its type in the
	 * database
	 */
	public static String convertData(String key, byte[] rawData)
			throws UnsupportedEncodingException {
		if (intColumns.contains(key)) {
			BigInteger value = getIntValue(rawData);
			String valueStr = applyIntMapping(key, value);
			return valueStr;
		} else if (strColumns.contains(key)) {
			return getStringValue(rawData);
		} else if (key.equals("destip") || key.equals("sourceip")) {
			long value = getLongValue(rawData);
			return longToIp(value);
		} else if (key.equals("teardown_time") || key.equals("setup_time")) {
			long epoch = getIntValue(rawData).longValue();
			String date = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
					.format(new java.util.Date(epoch / 1000));
			return date.replace(" ", "T");
		} else {
			return "";
		}
	}

	/*
	 * FUNCTION: applyIntMapping(key,value) this function takes a key string and
	 * an integer value and converts them if a mapping is available for them
	 * otherwise it just converts the given integer to a string
	 */
	private static String applyIntMapping(String key, BigInteger value) {
		if (key.equals("protocol")) {
			/* converting protocol number to protocol name */
			return getprotobynumber(value.intValue());
		} else {
			return String.valueOf(value);
		}
	}

	/*
	 * FUNCTION: longToIp(Long IpAddress) It will convert a given ip from long
	 * to the standard string format
	 */
	public static String longToIp(long ip) {
		return ((ip >> 24) & 0xFF) + "." + ((ip >> 16) & 0xFF) + "."
				+ ((ip >> 8) & 0xFF) + "." + (ip & 0xFF);
	}

	/*
	 * FUNCTION: getIntValueStr(rawDara) It takes data in the form of bytes and
	 * converts it into an Int and returns its string form
	 */
	public static BigInteger getIntValue(byte[] rawData) {
		return new BigInteger(rawData);
	}

	/*
	 * FUNCTION: getLongValueStr(rawDara) It takes data in the form of bytes and
	 * converts it into an Int and returns its string form
	 */
	public static int getLongValue(byte[] rawData) {
		return ByteBuffer.wrap(rawData).getInt();
	}

	/*
	 * FUNCTION: getIntValueStr(rawDara) It takes data in the form of bytes and
	 * converts it into an Int and returns its string form
	 */
	public static String getIntValueStr(byte[] rawData) {
		BigInteger value = getIntValue(rawData);
		return String.valueOf(value);
	}

	/*
	 * FUNCTION: getShortValueStr(rawDara) It takes data in the form of bytes
	 * and converts it into a short and returns its string form
	 */
	public static String getShortValueStr(ByteBuffer rawDataBuf) {
		return String.valueOf(rawDataBuf.get() & 0xff);
	}

	/*
	 * FUNCTION: getStringValue(rawDara) It takes data in the form of bytes and
	 * converts it into a string in ASCII format
	 */
	public static String getStringValue(byte[] rawData)
			throws UnsupportedEncodingException {
		return new String(rawData, "US-ASCII");
	}

	public static String getprotobynumber(int protoNumber) {
		for (Map.Entry<String, Long> entry : protoToNum.entrySet())
			if (entry.getValue() == protoNumber)
				return entry.getKey();

		return String.valueOf(protoNumber);
	}
}
