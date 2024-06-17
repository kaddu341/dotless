import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.ArrayList;
import java.util.List;
import java.lang.Character;

public class DotsPredictor {

    // instance variables
    String[] wordlist;
    Map<Character, String[]> dotMap = new HashMap<Character, String[]>();

    //constructor
    public DotsPredictor(String filename) {

        // first: find number of lines in file
        int numLines = 0;
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            while (reader.readLine() != null) numLines++;
            reader.close();
        } catch (IOException e) {
            System.out.println("An I/O exception has occurred");
        }
        /*System.out.println(numLines);*/ // debug statement, to be removed

        // next: read file into an Array
        wordlist = new String[numLines];
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            int index = 0;
            String line = br.readLine();
            while (line != null) {
               wordlist[index] = line;
               line = br.readLine();
               index++;
            }
        } catch (IOException e) {
            System.out.println("An I/O exception has occurred");
        }
        /*System.out.println(wordlist[9196214]);*/ // debug statement, to be removed

        /*System.out.println(Arrays.binarySearch(wordlist, "يينعنها"));*/ // debug statement, to be removed

        // initialize values of dotless-to-dotted map
        dotMap.put('ا', new String[]{"ا", "أ", "إ", "آ", "ء", "اء", "آء"});
        dotMap.put('ٮ', new String[]{"ب", "ت", "ث"});
        dotMap.put('ح', new String[]{"ج", "ح", "خ"});
        dotMap.put('د', new String[]{"د", "ذ"});
        dotMap.put('ر', new String[]{"ر", "ز"});
        dotMap.put('س', new String[]{"س", "ش"});
        dotMap.put('ص', new String[]{"ص", "ض"});
        dotMap.put('ط', new String[]{"ط", "ظ"});
        dotMap.put('ع', new String[]{"ع", "غ"});
        dotMap.put('ڡ', new String[]{"ف", "ق"});
        dotMap.put('ك', new String[]{"ك"});
        dotMap.put('ل', new String[]{"ل"});
        dotMap.put('م', new String[]{"م"});
        dotMap.put('ن', new String[]{"ن"});
        dotMap.put('و', new String[]{"و", "ؤ", "وء"});
        dotMap.put('ه', new String[]{"ه"});
        dotMap.put('ى', new String[]{"ي", "ى", "ئ", "يء"});

        /*
        for(String str : dotMap.get('ا')) { // debug statement, to be removed later
            System.out.print(str + " ");
        }*/
    }
    
    public String[] getCandidates(String dotlessWord) {
        
        // first: find total number of variations
        int length = dotlessWord.length();
        int[] vars = new int[length];
        for (short i = 0; i < length; i++) {
            vars[i] = dotMap.get(dotlessWord.charAt(i)).length;
        }
        int numVariations = 1;
        for(int n : vars) {
            numVariations *= n;
        }

        String[] allVariations = new String[numVariations];

        // populate the array with all possible variations of the dotless word
        for(int i = 0; i < numVariations; i++) {    // one iteration for every possible word outcome
            String temporary = "";
            int carry = i;
            int num = numVariations;

            for(int j = 0; j < (length - 1); j++) {   //iterating over letters in dotless word
                num = num / vars[j];
                temporary += dotMap.get(dotlessWord.charAt(j))[carry / num];
                carry = carry % num;
            }
            // deal with the last letter
            /*System.out.println(carry);*/ // debug statement, to be removed later
            temporary += dotMap.get(dotlessWord.charAt(length - 1))[carry];

            // add to array
            allVariations[i] = temporary;
        }

        // now, after array is populated, find all entries that are valid Arabic words (i.e. they exist in the dictionary)
        List<String> candidates = new ArrayList<String>();
        for(String word : allVariations) {
            if(Arrays.binarySearch(wordlist, word) >= 0) {
                candidates.add(word);
            }
        }

        // cast to Array and return
        String[] strArray = {};
        return candidates.toArray(strArray);
    }

    public String[] getWordlist() {
        return wordlist;
    }

    public static void main(String[] args) {
        DotsPredictor dotsPredictor = new DotsPredictor("arabic-wordlist-sorted.txt");
        String dotlessWord = "حٮل";
        String[] allVariations = dotsPredictor.getCandidates(dotlessWord);
        System.out.println("Dotless Word: " + dotlessWord + "\nDotted Variations:");
        for (String word : allVariations) {
            System.out.println(word);
        }
    }
}