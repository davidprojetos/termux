package com.example.apifire;

import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import android.content.Intent;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import java.util.ArrayList;

public class PortfolioFragment extends Fragment {

    private ItemListManager itemListManager;
    private ImageView imageViewQuizz;
    private NumberSorter numberSorter;
    private PomodoroTimer pomodoroTimer;

    private EditText editTextId, editTextNome;
    private Button buttonAdicionar, buttonAtualizar, buttonDeletar;
    private ListView listViewItems;

    private EditText editTextIdSqlite, editTextNomeSqlite;
    private Button buttonAdicionarSqlite, buttonAtualizarSqlite, buttonDeletarSqlite;
    private ListView listViewItemsSqlite;
    private ArrayAdapter<String> listAdapterSqlite;
    private ArrayList<String> itemsListSqlite;
    private SQLiteHelper sqliteHelper;
    
    /*
    private EditText editTextInterval;
    private Button buttonStartNotifications, buttonStopNotifications;
    private BibleNotificationManager bibleNotificationManager;
    private Handler handler = new Handler();
    private Runnable notificationRunnable;
    private long intervalMillis;
    */
    
    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_portfolio, container, false);

        listViewItems = rootView.findViewById(R.id.listViewItems);
        editTextId = rootView.findViewById(R.id.editTextId);
        editTextNome = rootView.findViewById(R.id.editTextNome);
        buttonAdicionar = rootView.findViewById(R.id.buttonAdicionar);
        buttonAtualizar = rootView.findViewById(R.id.buttonAtualizar);
        buttonDeletar = rootView.findViewById(R.id.buttonDeletar);
        itemListManager = new ItemListManager(listViewItems, editTextId, editTextNome, buttonAdicionar, buttonAtualizar, buttonDeletar, this);

        imageViewQuizz = rootView.findViewById(R.id.imageViewQuizz);
        imageViewQuizz.setOnClickListener(v -> abrirWebView());

        TextView textViewUltimoSorteado = rootView.findViewById(R.id.textViewUltimoSorteado);
        ListView listViewNumerosSorteados = rootView.findViewById(R.id.listViewNumerosSorteados);
        Button buttonSortear = rootView.findViewById(R.id.buttonSortear);
        numberSorter = new NumberSorter(textViewUltimoSorteado, listViewNumerosSorteados, buttonSortear);

        TextView textViewTimer = rootView.findViewById(R.id.textViewTimer);
        Button buttonPlay = rootView.findViewById(R.id.buttonPlay);
        Button buttonPause = rootView.findViewById(R.id.buttonPause);
        Button buttonStop = rootView.findViewById(R.id.buttonStop);
        pomodoroTimer = new PomodoroTimer(textViewTimer, buttonPlay, buttonPause, buttonStop);

        listViewItemsSqlite = rootView.findViewById(R.id.listViewItemsSqlite);
        editTextIdSqlite = rootView.findViewById(R.id.editTextIdSqlite);
        editTextNomeSqlite = rootView.findViewById(R.id.editTextNomeSqlite);
        buttonAdicionarSqlite = rootView.findViewById(R.id.buttonAdicionarSqlite);
        buttonAtualizarSqlite = rootView.findViewById(R.id.buttonAtualizarSqlite);
        buttonDeletarSqlite = rootView.findViewById(R.id.buttonDeletarSqlite);
        sqliteHelper = new SQLiteHelper(getContext());

        itemsListSqlite = new ArrayList<>();
        listAdapterSqlite = new ArrayAdapter<>(getContext(), android.R.layout.simple_list_item_1, itemsListSqlite);
        listViewItemsSqlite.setAdapter(listAdapterSqlite);

        buttonAdicionarSqlite.setOnClickListener(v -> addItemSqlite());
        buttonAtualizarSqlite.setOnClickListener(v -> updateItemSqlite());
        buttonDeletarSqlite.setOnClickListener(v -> deleteItemSqlite());
        
        /*
        editTextInterval = rootView.findViewById(R.id.editTextInterval);
        buttonStartNotifications = rootView.findViewById(R.id.buttonStartNotifications);
        buttonStopNotifications = rootView.findViewById(R.id.buttonStopNotifications);

        buttonStartNotifications.setOnClickListener(v -> startBibleNotifications());
        buttonStopNotifications.setOnClickListener(v -> stopBibleNotifications());
        */
        loadItemsSqlite();

        return rootView;
    }

    public void abrirWebView() {
        Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://david-ds.rf.gd/sistema-questoes/"));
        startActivity(browserIntent);
    }

    private void addItemSqlite() {
        String name = editTextNomeSqlite.getText().toString();
        if (name.isEmpty()) {
            Toast.makeText(getContext(), "Nome não pode ser vazio", Toast.LENGTH_SHORT).show();
            return;
        }
        boolean result = sqliteHelper.addItemSqlite(name);
        if (result) {
            Toast.makeText(getContext(), "Item adicionado", Toast.LENGTH_SHORT).show();
            loadItemsSqlite();
        } else {
            Toast.makeText(getContext(), "Erro ao adicionar item", Toast.LENGTH_SHORT).show();
        }
    }

    private void updateItemSqlite() {
        String idStr = editTextIdSqlite.getText().toString();
        String name = editTextNomeSqlite.getText().toString();
        if (idStr.isEmpty() || name.isEmpty()) {
            Toast.makeText(getContext(), "ID e Nome não podem ser vazios", Toast.LENGTH_SHORT).show();
            return;
        }
        int id = Integer.parseInt(idStr);
        boolean result = sqliteHelper.updateItemSqlite(id, name);
        if (result) {
            Toast.makeText(getContext(), "Item atualizado", Toast.LENGTH_SHORT).show();
            loadItemsSqlite();
        } else {
            Toast.makeText(getContext(), "Erro ao atualizar item", Toast.LENGTH_SHORT).show();
        }
    }

    private void deleteItemSqlite() {
        String idStr = editTextIdSqlite.getText().toString();
        if (idStr.isEmpty()) {
            Toast.makeText(getContext(), "ID não pode ser vazio", Toast.LENGTH_SHORT).show();
            return;
        }
        int id = Integer.parseInt(idStr);
        boolean result = sqliteHelper.deleteItemSqlite(id);
        if (result) {
            Toast.makeText(getContext(), "Item deletado", Toast.LENGTH_SHORT).show();
            loadItemsSqlite();
        } else {
            Toast.makeText(getContext(), "Erro ao deletar item", Toast.LENGTH_SHORT).show();
        }
    }

    private void loadItemsSqlite() {
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
    /*
    private void startBibleNotifications() {
        intervalMillis = Long.parseLong(editTextInterval.getText().toString()) * 1000;

        notificationRunnable = new Runnable() {
            @Override
            public void run() {
                sendBibleNotification();
                handler.postDelayed(this, intervalMillis);
            }
        };
        handler.post(notificationRunnable);
        Toast.makeText(getContext(), "Notificações iniciadas", Toast.LENGTH_SHORT).show();
    }

    private void stopBibleNotifications() {
        handler.removeCallbacks(notificationRunnable);
        Toast.makeText(getContext(), "Notificações paradas", Toast.LENGTH_SHORT).show();
    }

    private void sendBibleNotification() {
        bibleNotificationManager = new BibleNotificationManager();
        bibleNotificationManager.showNotification(getContext(), "Your message");
    }*/
}
