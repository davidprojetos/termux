# db.rb
require 'mongo'

Mongo::Logger.logger.level = Logger::INFO # Configura o nível de log

client = Mongo::Client.new(['127.0.0.1:27017'], :database => 'david')

DB = client.database
