package com.example.apifire;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.PUT;
import retrofit2.http.Path;

public interface ApiService {
    @GET("items")
    Call<List<Item>> getItems();

    @POST("items")
    Call<Item> createItem(@Body Item item);

    @PUT("items/{id}")
    Call<Item> updateItem(@Path("id") String id, @Body Item item);

    @DELETE("items/{id}")
    Call<Void> deleteItem(@Path("id") String id); // Alterado para Call<Void>
}
