import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Train {

	public static void main(String[] args) throws IOException, ClassNotFoundException, Exception, InterruptedException {
		Configuration conf = new Configuration();
		// System.setProperty("hadoop.home.dir", "D:\\hadoop-2.5.2");
		// conf.set("fs.defaultFS", "hdfs://106.13.58.66:9000");
		Job job = Job.getInstance(conf);
		job.setJarByClass(Train.class);
		job.setMapperClass(wordMapper.class);
		job.setReducerClass(wordReducer.class);
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(LongWritable.class);
		job.setCombinerClass(wordReducer.class);
		job.waitForCompletion(true);
	}

}
