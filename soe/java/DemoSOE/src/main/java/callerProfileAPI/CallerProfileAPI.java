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

import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

public class CallerProfileAPI {

    private static Logger log = Logger.getLogger(CallerProfileAPI.class.getName());
    private String fileName;
    private CSVHandler reader;

    /**
     * Constructor where the .csv file name is set
     */
    public CallerProfileAPI() {
        reader = new CSVHandler();
    }

    /**
     * Get the data for the caller profiles in the csv file and convert them to
     * callerProfiles
     * 
     * @return List of CallerProfiles made from data in the csv file
     */
    public ArrayList<CallerProfile> readProfiles() {
        if (log.isLoggable(Level.FINE)) {
            log.fine("Reading profiles from CSV");
        }
        return reader.readCSV();
    }

    /**
     * Write the Profiles to the csv file, wiping away the old ones
     * 
     * @param newProfiles
     *            The list of new profiles to add
     */
    public void writeProfiles(ArrayList<CallerProfile> newProfiles) {
        if (log.isLoggable(Level.FINE)) {
            log.fine("Writing profiles to CSV");
        }

        reader.writeCSV(newProfiles);
        return;
    }

    /**
     * Find a profile with the given name if it exists
     * 
     * @param name
     *            The name to match to a profile
     * @return The profile found with the name, null if not found
     */
    public CallerProfile getProfileByName(String name) {
        ArrayList<CallerProfile> profiles = readProfiles();
        CallerProfile profile = findProfileByFirstName(profiles, name);
        return profile;
    }

    /**
     * Search the profiles to find one for a given name
     * 
     * @param nameIn
     *            Name of user in profile to search for
     */
    public CallerProfile findProfileByFirstName(ArrayList<CallerProfile> profiles, String nameIn) {
        for (int i = 0; i < profiles.size(); i++) {
            if (profiles.get(i).getFirstname().equals(nameIn)) {
                if (log.isLoggable(Level.FINE)) {
                    log.fine("Profile Found: " + profiles.get(i).getFirstname());
                }
                return profiles.get(i);
            }
        }

        return null;
    }

    /**
     * Update a profile in the csv file based on the name. In case of duplicate
     * names, updates all the profiles with that name
     * 
     * @param profile
     *            The profile with the updated information
     */
    public void updateProfile(CallerProfile profile) {
        if (log.isLoggable(Level.FINE)) {
            log.fine("Updating profile: " + profile.getFirstname());
        }
        ArrayList<CallerProfile> profiles = readProfiles();

        for (int i = 0; i < profiles.size(); i++) {
            if (profiles.get(i).getFirstname().equals(profile.getFirstname())) {
                profiles.set(i, profile);
                writeProfiles(profiles);
                return;
            }
        }
        if (log.isLoggable(Level.FINE)) {
            log.fine("No profile found");
        }
    }

    /**
     * Take money from an account and use it to pay off part of a loan. Only
     * allow payments where the amount being paid is less than or equal to the
     * total loan amount and the account balance.
     * 
     * @param profile
     *            Profile to carryout transaction
     * @param loan
     *            Type of loan to put money to
     * @param Account
     *            Account to withdraw money from
     * @param amount
     *            Amount to transfer
     * @return If transaction was successful
     */
    public boolean makePayment(CallerProfile profile, String loan, String Account, int amount) {
        if (log.isLoggable(Level.FINE)) {
            log.fine("Making payment for:" + profile.getFirstname() + "\nFrom: " + Account + "\nTo: " + loan
                    + "\nFor: $" + Integer.toString(amount));
        }
        if (profile.hasLoanType(loan)) {
            if (profile.getLoanBalance(loan) >= amount && profile.getAccountBalance(Account) >= amount) {
                profile.setAccountBalance(Account, profile.getAccountBalance(Account) - amount);
                profile.setLoanBalance(loan, profile.getLoanBalance(loan) - amount);
                return true;
            }
        }
        if (log.isLoggable(Level.FINE)) {
            log.fine("Payment failed");
        }
        return false;
    }

    /**
     * Create a new card number for a card type given a profile
     */
    public void addNewCard(CallerProfile profile, String cardType, String cardNumber) {
        profile.setCardNumber(cardType, cardNumber);
    }

    /**
     * Sets up tests with dummy profiles written to the csv
     */
    public void writeStandardProfiles() {
        ArrayList<CallerProfile> addProfs = new ArrayList<CallerProfile>();

        // Dummy profiles
        CallerProfile test0 = new CallerProfile("A", "a", 1000, 0, 0, 500, 0, 0, 0, 0, 0);
        CallerProfile test1 = new CallerProfile("B", "b", 1, 1, 1, 1, 1, 1, 1, 1, 2);
        CallerProfile test2 = new CallerProfile("C", "C", 2, 2, 2, 2, 2, 2, 2, 2, 2);
        CallerProfile test3 = new CallerProfile("D", "D", 3, 3, 3, 3, 3, 3, 3, 3, 3);
        addProfs.add(test0);
        addProfs.add(test1);
        addProfs.add(test2);
        addProfs.add(test3);

        // Write them to csv
        writeProfiles(addProfs);
    }

    /**
     * Give the profiles list used in testing
     * 
     * @return List of profiles used for testing
     */
    public ArrayList<CallerProfile> getStandardProfiles() {
        ArrayList<CallerProfile> addProfs = new ArrayList<CallerProfile>();

        // Dummy profiles
        CallerProfile test0 = new CallerProfile("A", "a", 1000, 0, 0, 500, 0, 0, 0, 0, 0);
        CallerProfile test1 = new CallerProfile("B", "b", 1, 1, 1, 1, 1, 1, 1, 1, 2);
        CallerProfile test2 = new CallerProfile("C", "C", 2, 2, 2, 2, 2, 2, 2, 2, 2);
        CallerProfile test3 = new CallerProfile("D", "D", 3, 3, 3, 3, 3, 3, 3, 3, 3);
        addProfs.add(test0);
        addProfs.add(test1);
        addProfs.add(test2);
        addProfs.add(test3);

        return addProfs;
    }

    // Getters and Setters

    public String getFileName() {
        return fileName;
    }

    public void setFileName(String fileName) {
        this.fileName = fileName;
    }
}