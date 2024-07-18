// PortfolioItem.java
package com.example.apifire;

public class PortfolioItem {
    private String title;
    private String description;
    private int imageResId;

    public PortfolioItem(String title, String description, int imageResId) {
        this.title = title;
        this.description = description;
        this.imageResId = imageResId;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public int getImageResId() {
        return imageResId;
    }
}
