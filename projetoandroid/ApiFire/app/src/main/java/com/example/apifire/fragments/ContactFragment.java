package com.example.apifire.fragments;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.example.apifire.R;
import com.example.apifire.project.EnvioEmail;

public class ContactFragment extends Fragment {

    private EnvioEmail envioEmail;
    private EditText editTextRecipient, editTextName, editTextSubject, editTextMessage;
    private Button buttonSend;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_contact, container, false);

        editTextRecipient = view.findViewById(R.id.editTextRecipient);
        editTextName = view.findViewById(R.id.editTextName);
        editTextSubject = view.findViewById(R.id.editTextSubject);
        editTextMessage = view.findViewById(R.id.editTextMessage);
        buttonSend = view.findViewById(R.id.buttonSend);

        // Passar o contexto da fragment para EnvioEmail
        envioEmail = new EnvioEmail(editTextRecipient, editTextName, editTextSubject, editTextMessage, buttonSend, getContext());

        return view;
    }
}
