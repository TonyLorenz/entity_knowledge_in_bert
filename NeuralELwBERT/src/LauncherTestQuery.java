
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintStream;
import java.util.Iterator;
import java.util.List;

import org.apache.jena.query.Dataset;
import org.apache.jena.query.Query;
import org.apache.jena.query.QueryExecution;
import org.apache.jena.query.QueryExecutionFactory;
import org.apache.jena.query.QueryFactory;
import org.apache.jena.query.QuerySolution;
import org.apache.jena.query.ResultSet;
import org.apache.jena.rdf.model.Model;
import org.apache.jena.tdb.TDBFactory;

import com.google.common.base.Charsets;
import com.google.common.collect.Lists;
import com.google.common.io.Files;

import au.com.bytecode.opencsv.CSVWriter;

public class LauncherTestQuery {

	public static void main(String[] args) {
		// Folder with queries to execute
		final String inFolderPath = "./query_in/";
		System.out.println("Running queries from: " + inFolderPath);

		// Dataset
		final String datasetPath = "./triple_database.tdb";
		final Dataset dataset = TDBFactory.createDataset(datasetPath);
		System.out.println("Finished loading!");

		// Model
		final Model model = dataset.getDefaultModel();
		try {
//		final String queryStr = "select distinct ?s (CONCAT(CONCAT(?fname, \" \"), ?lname) AS ?o) where {\r\n"
//				+ "?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ontologycentral.com/2010/05/cb/vocab#Person> .\r\n"
//				+ "?s <http://ontologycentral.com/2010/05/cb/vocab#last_name> ?lname .\r\n"
//				+ "?s <http://ontologycentral.com/2010/05/cb/vocab#first_name> ?fname .\r\n" + "}";
			System.out.println("Executing queries from folder [" + inFolderPath + "] ...");

			final File inFolder = new File(inFolderPath);
			if (!inFolder.isDirectory() || !inFolder.exists()) {
				throw new FileNotFoundException("Could not find directory [" + inFolderPath + "]...");
			}
			final File[] files = inFolder.listFiles();
			/*PrintStream oldOut = System.out;*/
			for (File file : files) {
				final String queryStr = getContents(file);
				/*
				try (final PrintStream fos = new PrintStream(
						new FileOutputStream(new File(file.getName() + "_out"), false))) {
					System.setOut(fos);
				}*/
				execQuery(model, queryStr, file);
			}
			/*System.setOut(oldOut);*/
			
			
			
			
			
			// getABC(model);
			// getObjectsFor(model, "http://dbpedia.org/resource/Smartphone");
			// getObjectsForSubjectOfSFQuery(model,
			// "http://dbpedia.org/resource/Smartphone");
//		Stopwatch.endOutputStart(LauncherTestQuery.class.getName());
			// getPredicates(model);
			// Stopwatch.endOutputStart(LauncherTestQuery.class.getName());
			// getTypes(model);
			// Stopwatch.endOutputStart(LauncherTestQuery.class.getName());
			// getPredicatesGroupCounts(model);
			// Stopwatch.endOutputStart(LauncherTestQuery.class.getName());
			// getRandom(model);
			// testVirtuoso();
			// getDBLPAuthors(model);
			// getSteveJobsConnections(model);
			// getCrunchbaseNews(model);
			// getPredicatesAndTypes(model);
		} catch (Exception e) {

		} finally {
			model.close();
			dataset.close();
		}

		System.out.println("Finished!");
		// "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 100"
	}

	private static void execQuery(Model model, String queryStr, File inFile) {
		System.out.println("Executing query from [" + inFile.getAbsolutePath() + "]");
		System.out.println(queryStr);
		final ResultSet results = execQuerySelect(model, queryStr);
		final String outFolderPath = inFile.getParentFile().getParentFile().getAbsolutePath() + "/" + "query_out";
		final File outFolder = new File(outFolderPath);
		if (!outFolder.exists()) {
			outFolder.mkdirs();
		}
		final File outFile = new File(outFolder.getAbsolutePath() + "/" + inFile.getName() + "_out");
		System.out.println("Outputting results to: " + outFile.getAbsolutePath());
		saveQuery(results, outFile);
		// displayQuery(results);
	}

	private static void saveQuery(ResultSet results, File outFile) {
		try (final CSVWriter csvWrt = new CSVWriter(new FileWriter(outFile))) {
			while (results.hasNext()) {
				final QuerySolution qs = results.next();
				final Iterator<String> it = new QuerySolutionIterator(qs);
				// Iterator<String> it = qs.varNames();

				final List<String> line = Lists.newArrayList();
				while (it.hasNext()) {
					final String varName = it.next();
					line.add(qs.get(varName).toString());
					// System.out.print(varName + ":" + qs.get(varName) + " ");
				}
				csvWrt.writeNext(line.toArray(new String[] {}));
				// System.out.println();
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	private static void displayQuery(ResultSet results) {
		while (results.hasNext()) {
			final QuerySolution qs = results.next();
			// Iterator<String> it = new de.dwslab.petar.walks.QuerySolutionIterator(qs);
			Iterator<String> it = qs.varNames();
			while (it.hasNext()) {
				final String varName = it.next();
				System.out.print(varName + ":" + qs.get(varName) + " ");
			}
			System.out.println();
		}
	}

	public static String getContents(final File file) throws IOException {
		return Files.asCharSource(file, Charsets.UTF_8).read();
	}

	public static ResultSet execQuerySelect(Model model, String queryStr) {
		// System.out.println("Executing");
		// System.out.println(queryStr);
		final Query query = QueryFactory.create(queryStr);
		// Execute the query and obtain results
		final QueryExecution qe = QueryExecutionFactory.create(query, model);
		final ResultSet results = qe.execSelect();
		return results;
	}

}
