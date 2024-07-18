# app.rb
require 'sinatra'
require 'json'
require 'mongo'

# Configurar a conexão com o MongoDB
client = Mongo::Client.new(['127.0.0.1:27017'], database: 'test')
DB = client.database

helpers do
  def json_params
    begin
      JSON.parse(request.body.read)
    rescue
      halt 400, { message: 'Invalid JSON' }.to_json
    end
  end

  def document_to_hash(document)
    document.inject({}) do |hash, (key, value)|
      hash[key.to_s] = value
      hash
    end
  end
end

get '/api/v1/items' do
  content_type :json
  items = DB[:items].find.map { |item| document_to_hash(item) }
  items.to_json
end

get '/api/v1/items/:id' do
  content_type :json
  item = DB[:items].find(_id: BSON::ObjectId(params[:id])).first
  if item
    document_to_hash(item).to_json
  else
    halt 404, { message: 'Item not found' }.to_json
  end
end

post '/api/v1/items' do
  content_type :json
  item = json_params
  result = DB[:items].insert_one(item)
  if result.n == 1
    { message: 'Item created successfully' }.to_json
  else
    halt 500, { message: 'Failed to create item' }.to_json
  end
end

delete '/api/v1/items/:id' do
  content_type :json
  result = DB[:items].delete_one(_id: BSON::ObjectId(params[:id]))
  if result.deleted_count == 1
    { message: 'Item deleted successfully' }.to_json
  else
    halt 404, { message: 'Item not found' }.to_json
  end
end
