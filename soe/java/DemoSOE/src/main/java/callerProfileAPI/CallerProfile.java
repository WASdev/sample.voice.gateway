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

import java.util.logging.Level;
import java.util.logging.Logger;

public class CallerProfile {
    private static Logger log = Logger.getLogger(CallerProfile.class.getName());

    
    private String firstname;
    private String passcode;
    private int checkingAmt;
    private int savingAmt;
    private int moneyMarketAmt;
    private int autoLoanAmt;
    private int studentLoanAmt;
    private int mortgageAmt;
    private int autoLoanPayAmt;
    private int studentLoanPayAmt;
    private int mortgagePayAmt;
    private String discoverCardNumber;
    private String masterCardNumber;
    private String visaCardNumber;
    private String americanExpressCardNumber;

    /**
     * Constructor for creating profile from strings
     */
    public CallerProfile(String nameIn, String passIn, String checkIn, String saveIn, String mmIn, String autoIn,
            String studentIn, String mortIn, String aPIn, String sPIn, String mPIn) {
        firstname = nameIn;
        passcode = passIn;
        checkingAmt = Integer.parseInt(checkIn);
        savingAmt = Integer.parseInt(saveIn);
        moneyMarketAmt = Integer.parseInt(mmIn);
        autoLoanAmt = Integer.parseInt(autoIn);
        studentLoanAmt = Integer.parseInt(studentIn);
        mortgageAmt = Integer.parseInt(mortIn);
        autoLoanPayAmt = Integer.parseInt(aPIn);
        studentLoanPayAmt = Integer.parseInt(sPIn);
        mortgagePayAmt = Integer.parseInt(mPIn);
    }

    /**
     * Constructor for creating profile from Strings and ints
     */
    public CallerProfile(String nameIn, String passIn, int checkIn, int saveIn, int mmIn, int autoIn, int studentIn,
            int mortIn, int aPIn, int sPIn, int mPIn) {
        firstname = nameIn;
        passcode = passIn;
        checkingAmt = checkIn;
        savingAmt = saveIn;
        moneyMarketAmt = mmIn;
        autoLoanAmt = autoIn;
        studentLoanAmt = studentIn;
        mortgageAmt = mortIn;
        autoLoanPayAmt = aPIn;
        studentLoanPayAmt = sPIn;
        mortgagePayAmt = mPIn;

    }

    /**
     * Create profile from firstname and password
     */
    public CallerProfile(String firstname, String passcode) {
        this.firstname = firstname;
        this.passcode = passcode;
    }

    /**
     * Return if the user has the type of loan asked about
     * 
     * @param type
     *            Loan type
     * @return If the loan value is not 0
     */
    public boolean hasLoanType(String type) {
        if (type.contains("auto")) {
            return this.autoLoanAmt != 0;
        } else if (type.contains("student")) {
            return this.studentLoanAmt != 0;
        } else if (type.contains("mortgage")) {
            return this.mortgageAmt != 0;
        } else {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Checking if profile has loan type for invalid type " + type);
            }
        }
        return false;
    }

    /**
     * The amount in the desired account type
     * 
     * @param type
     *            Account to check balance of
     * @return Account balance
     */
    public int getAccountBalance(String type) {
        if (type.contains("checking")) {
            return checkingAmt;
        } else if (type.contains("savings")) {
            return savingAmt;
        } else if (type.contains("market")) {
            return moneyMarketAmt;
        }
        if (log.isLoggable(Level.FINE)) {
            log.fine("Attempt to get account balance for invalid type" + type);
        }
        return -1;
    }

    /**
     * Set the given account to the desired amount
     * 
     * @param type
     *            Type of account to change balance
     * @param newAmount
     *            New balance of the account
     */
    public void setAccountBalance(String type, int newAmount) {
        if (newAmount >= 0) {
            if (type.contains("checking")) {
                checkingAmt = newAmount;
            } else if (type.contains("savings")) {
                savingAmt = newAmount;
            } else if (type.contains("market")) {
                moneyMarketAmt = newAmount;
            } else {
                if (log.isLoggable(Level.FINE)) {
                    log.fine("Attempt to set account balance for invalid type" + type);
                }
            }
        } else {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Setting account balance to" + newAmount);
            }
        }
    }

    /**
     * The amount in the desired loan type if it exists
     * 
     * @param type
     *            Loan type to check balance of
     * @return Amount of the loan
     */
    public int getLoanBalance(String type) {
        if (type.contains("auto")) {
            return this.autoLoanAmt;
        } else if (type.contains("student")) {
            return this.studentLoanAmt;
        } else if (type.contains("mortgage")) {
            return this.mortgageAmt;
        } else {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Attempt to get balance for invalid type" + type);
            }
        }
        return -1;
    }

    /**
     * Set the given loan to the desired amount
     * 
     * @param type
     *            Type of loan to change amount
     * @param newAmount
     *            New Amount to set the loan to
     */
    public void setLoanBalance(String type, int newAmount) {
        if (newAmount >= 0) {
            if (type == "autoloan") {
                autoLoanAmt = newAmount;
            } else if (type == "studentloan") {
                studentLoanAmt = newAmount;
            } else if (type == "mortgage") {
                mortgageAmt = newAmount;
            } else {
                if (log.isLoggable(Level.FINE)) {
                    log.fine("Attempt to set loan balance for invalid type" + type);
                }
            }
        } else {
            if (log.isLoggable(Level.FINE)) {
                log.fine("Attempt to set loan balance for invalid type" + newAmount);
            }
        }
    }
    
    public void setCardNumber(String cardType, String cardNumber) {
        if(cardType.equalsIgnoreCase("mastercard") || cardType.equalsIgnoreCase("master card")) {
            masterCardNumber = cardNumber;
        }
        if(cardType.equalsIgnoreCase("discovercard") || cardType.equalsIgnoreCase("discover card")) {
            discoverCardNumber = cardNumber;
        }
        if(cardType.equalsIgnoreCase("visa")) {
            visaCardNumber = cardNumber;
        }
        if(cardType.equalsIgnoreCase("american express") || cardType.equalsIgnoreCase("american express")) {
            americanExpressCardNumber = cardNumber;
        }
    }

    /**
     * Print the contents of a CallerProfile
     * 
     * @Override
     * @return The callerProfile as a String
     */
    public String toString() {
        String output = "";

        output = "Name: " + firstname + "\nPassword: " + passcode + "\nCheckings: " + Integer.toString(checkingAmt)
                + "\nSavings: " + Integer.toString(savingAmt) + "\nMoneyMarket: " + Integer.toString(moneyMarketAmt)
                + "\nAutoLoan: " + Integer.toString(autoLoanAmt) + "\nStudentLoan: " + Integer.toString(studentLoanAmt)
                + "\nMortgage: " + Integer.toString(mortgageAmt) + "\nAutoLoan Payments: "
                + Integer.toString(autoLoanPayAmt) + "\nStudentLoan Payments: " + Integer.toString(studentLoanPayAmt)
                + "\nMortgage Payment: " + Integer.toString(mortgagePayAmt) + "\n\n" + "MasterCard: " + masterCardNumber;

        return output;
    }

    /**
     * Print the contents of a CallerProfile formatted neatly
     * 
     * @Override
     * @return The callerProfile as a String
     */
    public String toStringFormatted() {
        String output = "";
        StringBuilder sb = new StringBuilder();
        sb.append('\n');
        sb.append(firstname);
        sb.append(',');
        sb.append(passcode);
        sb.append(',');
        sb.append(Integer.toString(checkingAmt));
        sb.append(',');
        sb.append(Integer.toString(savingAmt));
        sb.append(',');
        sb.append(Integer.toString(moneyMarketAmt));
        sb.append(',');
        sb.append(Integer.toString(autoLoanAmt));
        sb.append(',');
        sb.append(Integer.toString(studentLoanAmt));
        sb.append(',');
        sb.append(Integer.toString(mortgageAmt));
        sb.append(',');
        sb.append(Integer.toString(autoLoanPayAmt));
        sb.append(',');
        sb.append(Integer.toString(studentLoanPayAmt));
        sb.append(',');
        sb.append(Integer.toString(mortgagePayAmt));
        sb.append(',');
        sb.append(masterCardNumber);
        sb.append(',');
        sb.append(visaCardNumber);
        sb.append(',');
        sb.append(discoverCardNumber);
        sb.append(',');
        sb.append(americanExpressCardNumber);

        output = sb.toString();

        return output;
    }

    // Getters & Setters

    public String getFirstname() {
        return firstname;
    }

    public void setFirstname(String firstname) {

        this.firstname = firstname;
    }

    public String getPasscode() {
        return passcode;
    }

    public void setPasscode(String passcode) {
        this.passcode = passcode;
    }

    public boolean equals(CallerProfile profile) {
        return profile.getFirstname().equals(firstname) && profile.getPasscode().equals(passcode)
                && profile.getAccountBalance("checking") == getAccountBalance("checking")
                && profile.getAccountBalance("savings") == getAccountBalance("savings")
                && profile.getAccountBalance("moneymarket") == getAccountBalance("moneymarket")
                && profile.getLoanBalance("autoloan") == getLoanBalance("autoloan")
                && profile.getLoanBalance("studentloan") == getLoanBalance("studentloan")
                && profile.getLoanBalance("mortgage") == getLoanBalance("mortgage");
    }
}
