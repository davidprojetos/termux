package com.example.apifire.models;

public class BiblePassage {
    private String title;
    private String passage;

    public BiblePassage(String title, String passage) {
        this.title = title;
        this.passage = passage;
    }

    public String getTitle() {
        return title;
    }

    public String getPassage() {
        return passage;
    }
}
