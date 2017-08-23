/**
* (C) Copyright IBM Corporation 2016.
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

package callerProfileAPI;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class CSVHandler {
    private String csvFile;
    private int csvLength;

    /**
     * Constructor
     * 
     * @param fileName
     *            File to be reading/writing
     */
    public CSVHandler() {
        csvFile = "/file/callerProfile.csv";
        csvLength = 0;
    }

    /**
     * Read the csv to extract the profile data
     * 
     * @return A 2d array of profile data
     */
    public ArrayList<CallerProfile> readCSV() {

        ClassLoader classLoader = getClass().getClassLoader();
        File f = new File(classLoader.getResource(csvFile).getFile());
        BufferedReader br = null;
        String line = "";
        String cvsSplitBy = ",";
        String dataOut[][] = new String[500][500];

        try {
            br = new BufferedReader(new FileReader(f));
        } catch (FileNotFoundException e1) {
            e1.printStackTrace();
        }

        try {
            br.readLine();
            int i = 0;
            while ((line = br.readLine()) != null) {

                // use comma as separator
                String[] data = line.split(cvsSplitBy);
                dataOut[i] = data;
                i++;
            }
            csvLength = i;

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
        return arrayToProfiles(dataOut);
    }

    /**
     * Append the new profiles to the csv file
     * 
     * @param profiles
     *            The Profiles to append
     */
    public void writeCSV(ArrayList<CallerProfile> profiles) {
        try {
            ClassLoader classLoader = getClass().getClassLoader();
            File f = new File(classLoader.getResource(csvFile).getFile());

            FileWriter pw = new FileWriter(f);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < profiles.size(); i++) {

                String line = profiles.get(i).toStringFormatted();
                sb.append(line);
            }
            pw.write(sb.toString());
            pw.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    /**
     * Get the number of real entries in the csv file. Updated after a read
     * 
     * @return Number of rows with data
     */
    public int getCSVLength() {
        return csvLength;
    }

    /**
     * Turns a 2d array of strings into an arraylist of profiles
     * 
     * @param profilesIn
     *            The array of profile information
     * @return ArrayList of CallerProfiles created from the data
     */
    public ArrayList<CallerProfile> arrayToProfiles(String[][] profilesIn) {
        String pData[];
        ArrayList<CallerProfile> profiles = new ArrayList<CallerProfile>();
        CallerProfile temp;

        for (int i = 0; i < getCSVLength(); i++) {
            pData = profilesIn[i];
            temp = new CallerProfile(pData[0], pData[1], pData[2], pData[3], pData[4], pData[5], pData[6], pData[7],
                    pData[8], pData[9], pData[10]);
            profiles.add(temp);
        }
        return profiles;
    }
}
