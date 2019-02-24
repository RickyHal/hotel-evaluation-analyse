import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class wordReducer extends Reducer<Text, LongWritable, Text, LongWritable> {
	@Override
	protected void reduce(Text key, Iterable<LongWritable> value,
			Reducer<Text, LongWritable, Text, LongWritable>.Context context) throws IOException, InterruptedException {
		long count = 0;

		for (LongWritable v : value) {
			count += v.get();
		}
		context.write(key, new LongWritable(count));
	}
}
