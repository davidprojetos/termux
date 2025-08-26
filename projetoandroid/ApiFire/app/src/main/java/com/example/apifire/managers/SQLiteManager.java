package com.example.apifire.managers;

import android.content.Context;
import android.database.Cursor;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

import android.view.View;
import android.widget.AdapterView;

import com.example.apifire.helpers.SQLiteHelper;

import java.util.ArrayList;

public class SQLiteManager {
    private EditText editTextIdSqlite, editTextNomeSqlite;
    private ArrayList<String> itemsListSqlite;
    private ArrayAdapter<String> listAdapterSqlite;
    private SQLiteHelper sqliteHelper;
    private Context context;

    public SQLiteManager(EditText editTextIdSqlite, EditText editTextNomeSqlite, ListView listViewItemsSqlite, SQLiteHelper sqliteHelper, Context context) {
        this.editTextIdSqlite = editTextIdSqlite;
        this.editTextNomeSqlite = editTextNomeSqlite;
        this.itemsListSqlite = new ArrayList<>();
        this.listAdapterSqlite = new ArrayAdapter<>(context, android.R.layout.simple_list_item_1, itemsListSqlite);
        listViewItemsSqlite.setAdapter(listAdapterSqlite);
        this.sqliteHelper = sqliteHelper;
        this.context = context;

        // Adiciona o OnItemClickListener ao ListView
        listViewItemsSqlite.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                String item = itemsListSqlite.get(position);
                String[] parts = item.split(": ");
                if (parts.length == 2) {
                    editTextIdSqlite.setText(parts[0]);
                    editTextNomeSqlite.setText(parts[1]);
                }
            }
        });
    }


    public void addItemSqlite() {
        String name = editTextNomeSqlite.getText().toString();
        if (name.isEmpty()) {
            Toast.makeText(context, "Nome não pode ser vazio", Toast.LENGTH_SHORT).show();
            return;
        }
        boolean result = sqliteHelper.addItemSqlite(name);
        if (result) {
            Toast.makeText(context, "Item adicionado", Toast.LENGTH_SHORT).show();
            loadItemsSqlite();
        } else {
            Toast.makeText(context, "Erro ao adicionar item", Toast.LENGTH_SHORT).show();
        }
    }

    public void updateItemSqlite() {
        String idStr = editTextIdSqlite.getText().toString();
        String name = editTextNomeSqlite.getText().toString();
        if (idStr.isEmpty() || name.isEmpty()) {
            Toast.makeText(context, "ID e Nome não podem ser vazios", Toast.LENGTH_SHORT).show();
            return;
        }
        int id = Integer.parseInt(idStr);
        boolean result = sqliteHelper.updateItemSqlite(id, name);
        if (result) {
            Toast.makeText(context, "Item atualizado", Toast.LENGTH_SHORT).show();
            loadItemsSqlite();
        } else {
            Toast.makeText(context, "Erro ao atualizar item", Toast.LENGTH_SHORT).show();
        }
    }

    public void deleteItemSqlite() {
        String idStr = editTextIdSqlite.getText().toString();
        if (idStr.isEmpty()) {
            Toast.makeText(context, "ID não pode ser vazio", Toast.LENGTH_SHORT).show();
            return;
        }
        int id = Integer.parseInt(idStr);
        boolean result = sqliteHelper.deleteItemSqlite(id);
        if (result) {
            Toast.makeText(context, "Item deletado", Toast.LENGTH_SHORT).show();
            loadItemsSqlite();
        } else {
            Toast.makeText(context, "Erro ao deletar item", Toast.LENGTH_SHORT).show();
        }
    }

    public void loadItemsSqlite() {
        itemsListSqlite.clear();
        Cursor cursor = sqliteHelper.getAllItemsSqlite();
        if (cursor.moveToFirst()) {
            do {
                int id = cursor.getInt(0);
                String name = cursor.getString(1);
                itemsListSqlite.add(id + ": " + name);
            } while (cursor.moveToNext());
        }
        cursor.close();
        listAdapterSqlite.notifyDataSetChanged();
    }
}
