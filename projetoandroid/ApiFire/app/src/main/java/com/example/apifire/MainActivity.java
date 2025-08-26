package com.example.apifire;

import android.os.Bundle;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;

import com.example.apifire.fragments.ContactFragment;
import com.example.apifire.fragments.FormattingFragment;
import com.example.apifire.fragments.HomeFragment;
import com.example.apifire.fragments.PortfolioFragment;
import com.google.android.material.bottomnavigation.BottomNavigationView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        BottomNavigationView bottomNavigationView = findViewById(R.id.bottom_navigation);
        bottomNavigationView.setSelectedItemId(R.id.menu_home);

        // Load the default fragment (HomeFragment)
        loadFragment(new HomeFragment());

        bottomNavigationView.setOnNavigationItemSelectedListener(item -> {
            Fragment selectedFragment = null;
            if (item.getItemId() == R.id.menu_formacao) {
                selectedFragment = new FormattingFragment();
            } else if (item.getItemId() == R.id.menu_contato) {
                selectedFragment = new ContactFragment();
            } else if (item.getItemId() == R.id.menu_portfolio) {
                selectedFragment = new PortfolioFragment();
            } else if (item.getItemId() == R.id.menu_home) {
                selectedFragment = new HomeFragment();
            }
            if (selectedFragment != null) {
                loadFragment(selectedFragment);
            }
            return true;
        });
    }

    private void loadFragment(Fragment fragment) {
        getSupportFragmentManager().beginTransaction()
                .replace(R.id.fragment_container, fragment)
                .commit();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == HomeFragment.REQUEST_CODE) {
            Fragment fragment = getSupportFragmentManager().findFragmentById(R.id.fragment_container);
            if (fragment != null) {
                fragment.onRequestPermissionsResult(requestCode, permissions, grantResults);
            }
        }
    }
}
