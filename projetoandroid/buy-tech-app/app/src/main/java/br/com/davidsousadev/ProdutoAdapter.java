package br.com.davidsousadev;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;

import java.util.List;

public class ProdutoAdapter extends RecyclerView.Adapter<ProdutoAdapter.ProdutoViewHolder> {

    private final Context context;
    private final List<Produto> produtos;

    public ProdutoAdapter(Context context, List<Produto> produtos) {
        this.context = context;
        this.produtos = produtos;
    }

    @NonNull
    @Override
    public ProdutoViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = LayoutInflater.from(context).inflate(R.layout.item_produto, parent, false);
        return new ProdutoViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ProdutoViewHolder holder, int position) {
        Produto p = produtos.get(position);
        holder.tvNome.setText(p.getNome());
        holder.tvDescricao.setText(p.getDescricao());
        holder.tvPreco.setText("R$" + p.getPreco());

        Glide.with(context)
             .load(p.getFoto())
             .into(holder.ivProduto);
    }

    @Override
    public int getItemCount() {
        return produtos.size();
    }

    static class ProdutoViewHolder extends RecyclerView.ViewHolder {
        ImageView ivProduto;
        TextView tvNome, tvDescricao, tvPreco;

        public ProdutoViewHolder(@NonNull View itemView) {
            super(itemView);
            ivProduto = itemView.findViewById(R.id.ivProduto);
            tvNome = itemView.findViewById(R.id.tvNome);
            tvDescricao = itemView.findViewById(R.id.tvDescricao);
            tvPreco = itemView.findViewById(R.id.tvPreco);
        }
    }
}