package com.example.apifire.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.example.apifire.models.BiblePassage;
import com.example.apifire.managers.LoginManager;
import com.example.apifire.R;
import com.example.apifire.helpers.SQLiteHelper;
import com.example.apifire.managers.ItemListManager;
import com.example.apifire.managers.QuizzManager;
import com.example.apifire.managers.SQLiteManager;
import com.example.apifire.project.BankSimulator;
import com.example.apifire.project.BiblePassageNotifier;
import com.example.apifire.project.NumberSorter;
import com.example.apifire.project.PomodoroTimer;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class PortfolioFragment extends Fragment {

    // Projeto 1 - API EXTERNA
    private ItemListManager itemListManager;
    private EditText editTextId, editTextNome;
    private Button buttonAdicionar, buttonAtualizar, buttonDeletar;
    private ListView listViewItems;

    // Projeto 2 - QUIZZ
    private ImageView imageViewQuizz;
    private QuizzManager quizzManager;

    // Projeto 3 - SORTEADOR
    private NumberSorter numberSorter;

    // Projeto 4 - POMODORO
    private PomodoroTimer pomodoroTimer;

    // Projeto 5 - CRUD SQLITE
    private EditText editTextIdSqlite, editTextNomeSqlite;
    private Button buttonAdicionarSqlite, buttonAtualizarSqlite, buttonDeletarSqlite;
    private ListView listViewItemsSqlite;
    private SQLiteHelper sqliteHelper;
    private SQLiteManager sqliteManager;

    // Projeto 6 - LOGIN E SENHA
    private EditText editTextUsername, editTextPassword;
    private Button buttonLogin;
    private LoginManager loginManager;

    // Projeto 7 - BANCO SIMULADOR
    private EditText editTextAccountNumber, editTextBalance;
    private Button buttonDeposit, buttonWithdraw;
    private ListView listViewTransactions;
    private BankSimulator bankSimulator;

    // Projeto 8 - NOTIFICAÇÕES BÍBLICAS
    private Button buttonStartNotifications, buttonStopNotifications;
    private BiblePassageNotifier biblePassageNotifier;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_portfolio, container, false);

        // Projeto 1 - API EXTERNA
        listViewItems = rootView.findViewById(R.id.listViewItems);
        editTextId = rootView.findViewById(R.id.editTextId);
        editTextNome = rootView.findViewById(R.id.editTextNome);
        buttonAdicionar = rootView.findViewById(R.id.buttonAdicionar);
        buttonAtualizar = rootView.findViewById(R.id.buttonAtualizar);
        buttonDeletar = rootView.findViewById(R.id.buttonDeletar);
        itemListManager = new ItemListManager(listViewItems, editTextId, editTextNome, buttonAdicionar, buttonAtualizar, buttonDeletar, this);

        // Projeto 2 - QUIZZ
        imageViewQuizz = rootView.findViewById(R.id.imageViewQuizz);
        quizzManager = new QuizzManager(getContext());
        imageViewQuizz.setOnClickListener(v -> quizzManager.abrirWebView());

        // Projeto 3 - SORTEADOR
        TextView textViewUltimoSorteado = rootView.findViewById(R.id.textViewUltimoSorteado);
        ListView listViewNumerosSorteados = rootView.findViewById(R.id.listViewNumerosSorteados);
        Button buttonSortear = rootView.findViewById(R.id.buttonSortear);
        numberSorter = new NumberSorter(textViewUltimoSorteado, listViewNumerosSorteados, buttonSortear);

        // Projeto 4 - POMODORO
        TextView textViewTimer = rootView.findViewById(R.id.textViewTimer);
        Button buttonPlay = rootView.findViewById(R.id.buttonPlay);
        Button buttonPause = rootView.findViewById(R.id.buttonPause);
        Button buttonStop = rootView.findViewById(R.id.buttonStop);
        pomodoroTimer = new PomodoroTimer(textViewTimer, buttonPlay, buttonPause, buttonStop);

        // Projeto 5 - CRUD SQLITE
        listViewItemsSqlite = rootView.findViewById(R.id.listViewItemsSqlite);
        editTextIdSqlite = rootView.findViewById(R.id.editTextIdSqlite);
        editTextNomeSqlite = rootView.findViewById(R.id.editTextNomeSqlite);
        buttonAdicionarSqlite = rootView.findViewById(R.id.buttonAdicionarSqlite);
        buttonAtualizarSqlite = rootView.findViewById(R.id.buttonAtualizarSqlite);
        buttonDeletarSqlite = rootView.findViewById(R.id.buttonDeletarSqlite);
        sqliteHelper = new SQLiteHelper(getContext());
        sqliteManager = new SQLiteManager(editTextIdSqlite, editTextNomeSqlite, listViewItemsSqlite, sqliteHelper, getContext());
        buttonAdicionarSqlite.setOnClickListener(v -> sqliteManager.addItemSqlite());
        buttonAtualizarSqlite.setOnClickListener(v -> sqliteManager.updateItemSqlite());
        buttonDeletarSqlite.setOnClickListener(v -> sqliteManager.deleteItemSqlite());
        sqliteManager.loadItemsSqlite();

        // Projeto 6 - LOGIN E SENHA
        editTextUsername = rootView.findViewById(R.id.editTextUsername);
        editTextPassword = rootView.findViewById(R.id.editTextPassword);
        buttonLogin = rootView.findViewById(R.id.buttonLogin);
        loginManager = new LoginManager(editTextUsername, editTextPassword, getContext());
        buttonLogin.setOnClickListener(v -> loginManager.performLogin());

        // Projeto 7 - BANCO SIMULADOR
        editTextAccountNumber = rootView.findViewById(R.id.editTextAccountNumber);
        editTextBalance = rootView.findViewById(R.id.editTextBalance);
        buttonDeposit = rootView.findViewById(R.id.buttonDeposit);
        buttonWithdraw = rootView.findViewById(R.id.buttonWithdraw);
        listViewTransactions = rootView.findViewById(R.id.listViewTransactions);
        bankSimulator = new BankSimulator(editTextAccountNumber, editTextBalance, listViewTransactions, getContext());
        buttonDeposit.setOnClickListener(v -> bankSimulator.performDeposit());
        buttonWithdraw.setOnClickListener(v -> bankSimulator.performWithdraw());

        // Projeto 8 - NOTIFICAÇÕES BÍBLICAS
        buttonStartNotifications = rootView.findViewById(R.id.buttonStartNotifications);
        buttonStopNotifications = rootView.findViewById(R.id.buttonStopNotifications);
        List<BiblePassage> biblePassages = new ArrayList<>();
        biblePassages.add(new BiblePassage("Salmos 23:1", "O Senhor é o meu pastor; nada me faltará."));
        biblePassages.add(new BiblePassage("Filipenses 4:13", "Tudo posso naquele que me fortalece."));
        biblePassages.add(new BiblePassage("João 3:16", "Porque Deus amou o mundo de tal maneira que deu o seu Filho unigênito, para que todo aquele que nele crê não pereça, mas tenha a vida eterna."));
        biblePassages.add(new BiblePassage("Romanos 8:28", "Sabemos que todas as coisas cooperam para o bem daqueles que amam a Deus."));
        biblePassages.add(new BiblePassage("Isaías 41:10", "Não temas, porque eu sou contigo; não te assombres, porque eu sou teu Deus."));
        biblePassages.add(new BiblePassage("Jeremias 29:11", "Porque sou eu que conheço os planos que tenho para vós, diz o Senhor; planos de paz e não de mal, para vos dar o fim que esperais."));
        biblePassages.add(new BiblePassage("Mateus 11:28", "Vinde a mim todos os que estais cansados e sobrecarregados, e eu vos aliviarei."));
        biblePassages.add(new BiblePassage("Salmos 119:105", "Lâmpada para os meus pés é a tua palavra e luz para o meu caminho."));
        biblePassages.add(new BiblePassage("Romanos 15:13", "Ora, o Deus de esperança vos encha de todo gozo e paz na vossa fé, para que abundéis em esperança pela potência do Espírito Santo."));
        biblePassages.add(new BiblePassage("1 Coríntios 13:13", "Agora, pois, permanecem a fé, a esperança e o amor, estes três; mas o maior destes é o amor."));
        biblePassages.add(new BiblePassage("João 14:6", "Disse-lhe Jesus: Eu sou o caminho, e a verdade, e a vida; ninguém vem ao Pai, senão por mim."));
        biblePassages.add(new BiblePassage("2 Timóteo 1:7", "Porque Deus não nos deu o espírito de temor, mas de fortaleza, e de amor, e de moderação."));
        biblePassages.add(new BiblePassage("Salmos 46:1", "Deus é o nosso refúgio e fortaleza, socorro bem presente na angústia."));
        biblePassages.add(new BiblePassage("Hebreus 13:5", "Seja a vossa vida sem avareza, contentando-vos com o que tendes, porque ele disse: Não te deixarei, nem te desampararei."));
        biblePassages.add(new BiblePassage("Gálatas 5:22-23", "Mas o fruto do Espírito é amor, alegria, paz, longanimidade, benignidade, bondade, fé, mansidão, temperança; contra estas coisas não há lei."));
        biblePassages.add(new BiblePassage("Efésios 2:8", "Porque pela graça sois salvos, por meio da fé; e isso não vem de vós, é dom de Deus."));
        biblePassages.add(new BiblePassage("Salmos 37:4", "Deleita-te também no Senhor, e ele te concederá o que deseja o teu coração."));
        biblePassages.add(new BiblePassage("1 João 4:7", "Amados, amemos uns aos outros, porque o amor é de Deus; e todo aquele que ama é nascido de Deus e conhece a Deus."));
        biblePassages.add(new BiblePassage("Tiago 1:5", "E, se algum de vós tem falta de sabedoria, peça-a a Deus, que a todos dá liberalmente e nada lhes impropera, e ser-lhe-á dada."));
        biblePassages.add(new BiblePassage("Colossenses 3:23", "E tudo o que fizerdes, fazei-o de todo o coração, como para o Senhor, e não para os homens."));
        biblePassages.add(new BiblePassage("Provérbios 3:5-6", "Confia no Senhor de todo o teu coração, e não te estribes no teu próprio entendimento. Reconhece-o em todos os teus caminhos, e ele endireitará as tuas veredas."));

        biblePassageNotifier = new BiblePassageNotifier(getContext(), biblePassages);

        buttonStartNotifications.setOnClickListener(v -> {
            long intervalMillis = TimeUnit.SECONDS.toMillis(5); // Timer
            biblePassageNotifier.startNotifications(intervalMillis);
            Toast.makeText(getContext(), "Notificações iniciadas!", Toast.LENGTH_SHORT).show();
        });

        buttonStopNotifications.setOnClickListener(v -> {
            biblePassageNotifier.stopNotifications();
            Toast.makeText(getContext(), "Notificações paradas!", Toast.LENGTH_SHORT).show();
        });

        return rootView;
    }
}
