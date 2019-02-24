import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class wordMapper extends Mapper<LongWritable, Text, Text, LongWritable> {
	@Override
	protected void map(LongWritable key, Text value, Mapper<LongWritable, Text, Text, LongWritable>.Context context)
			throws IOException, InterruptedException {
		String line = value.toString();
		// split line by \t,result is an array which 0 is type,1 is words
		String[] words = line.split("\t");
		// if this line has words
		if (words.length == 2) {
			// split the words
			words = words[1].split(" ");
			for (String word : words) {
				if (isChinese(word)) {
					// write "type_words 1"
					context.write(new Text(line.split("\t")[0] + "_" + word), new LongWritable(1));
					// write "type 1"
					// context.write(new Text(line.split("\t")[0]), new LongWritable(1));
				}
			}
		}
	}

	// check the words whether all is Chinese
	public boolean isChinese(String words) {
		int n = 0;
		for (int i = 0; i < words.length(); i++) {
			n = (int) words.charAt(i);
			if (!(19968 <= n && n < 40869)) {
				return false;
			}
		}
		return true;
	}
}
