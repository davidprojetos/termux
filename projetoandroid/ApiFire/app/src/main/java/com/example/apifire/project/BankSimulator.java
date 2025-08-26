package com.example.apifire.project;

import android.content.Context;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import java.util.ArrayList;

public class BankSimulator {
    private EditText editTextAccountNumber, editTextBalance;
    private ArrayList<String> transactionsList;
    private ArrayAdapter<String> listAdapterTransactions;
    private Context context;

    public BankSimulator(EditText editTextAccountNumber, EditText editTextBalance, ListView listViewTransactions, Context context) {
        this.editTextAccountNumber = editTextAccountNumber;
        this.editTextBalance = editTextBalance;
        this.transactionsList = new ArrayList<>();
        this.listAdapterTransactions = new ArrayAdapter<>(context, android.R.layout.simple_list_item_1, transactionsList);
        listViewTransactions.setAdapter(listAdapterTransactions);
        this.context = context;
    }

    public void performDeposit() {
        String accountNumber = editTextAccountNumber.getText().toString();
        String balanceStr = editTextBalance.getText().toString();
        if (accountNumber.isEmpty() || balanceStr.isEmpty()) {
            Toast.makeText(context, "Account Number and Balance cannot be empty", Toast.LENGTH_SHORT).show();
            return;
        }
        double balance = Double.parseDouble(balanceStr);
        transactionsList.add("Deposited: " + balance + " to account " + accountNumber);
        listAdapterTransactions.notifyDataSetChanged();
    }

    public void performWithdraw() {
        String accountNumber = editTextAccountNumber.getText().toString();
        String balanceStr = editTextBalance.getText().toString();
        if (accountNumber.isEmpty() || balanceStr.isEmpty()) {
            Toast.makeText(context, "Account Number and Balance cannot be empty", Toast.LENGTH_SHORT).show();
            return;
        }
        double balance = Double.parseDouble(balanceStr);
        transactionsList.add("Withdrew: " + balance + " from account " + accountNumber);
        listAdapterTransactions.notifyDataSetChanged();
    }
}
