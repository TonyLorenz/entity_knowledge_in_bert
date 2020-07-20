

import java.io.File;
import java.util.List;

import org.apache.jena.query.Dataset;
import org.apache.jena.query.ReadWrite;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.tdb.TDBFactory;
import org.apache.jena.tdb.TDBLoader;

import com.google.common.collect.Lists;

/**
 * Load a specified knowledge base into a Jena dataset that we can query
 * henceforth
 * 
 * @author Kris
 *
 */
public class LauncherSetupTDB {
	private static List<String> abortedList = Lists.newArrayList();

	public static void main(String[] args) {
		// new LauncherSetupTDB().exec();

		System.out.println("Setting up Triple Data Base!");
		final String KGpath =
				// WIKIDATA
				//"/vol2/wikidata/dumps/20190213/wikidata-20190213-truthy-BETA_all_URI-obj.nt"//
				
			"./input_files"
		;
		final File inFile = new File(KGpath);
		final List<String> inFiles = Lists.newArrayList();
		if (inFile.isDirectory()) {
			// Just takes files from the first level, does NOT go deeper if a directory is
			// contained within specified directory
			for (File f : inFile.listFiles()) {
				if (f.isFile()) {
					inFiles.add(f.getAbsolutePath());
				}
			}
		} else {
			inFiles.add(inFile.getAbsolutePath());
		}
		// Execute the loading part...
		for (String kgInPath : inFiles) {
			System.out.println("Source(" + (inFiles.indexOf(kgInPath) + 1) + "/" + inFiles.size() + "): " + kgInPath);
			new LauncherSetupTDB().exec(kgInPath);
			System.out.println("Aborted (" + abortedList.size() + "): " + abortedList);
		}

		System.out.println("Total Aborted files(" + abortedList.size() + "): " + abortedList);
		// Set up for other

	}

	/**
	 * Loads a single KG into the appropriate dataset
	 * 
	 * @param KG     which graph it corresponds to
	 * @param KGpath where to load it from
	 */
	public void exec(final String KGpath) {
		final String datasetPath = "./triple_database.tdb";
		// Non-empty file
		final Dataset dataset = TDBFactory.createDataset(datasetPath);
		dataset.begin(ReadWrite.READ);
		// Get model inside the transaction
		Model model = dataset.getDefaultModel();
		dataset.end();

		// Now load it all into the Model
		dataset.begin(ReadWrite.WRITE);
		model = dataset.getDefaultModel();
		try {
			TDBLoader.loadModel(model, KGpath, true);
			// model.commit();
			dataset.commit();
		} catch (Exception e) {
			System.out.println("Aborted: " + KGpath);
			abortedList.add(KGpath);
			// model.abort();
			dataset.abort();
		} finally {
			dataset.end();
		}
	}
}
