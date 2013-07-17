# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended to check this file into your version control system.

ActiveRecord::Schema.define(:version => 20130716080344) do

  create_table "articles", :force => true do |t|
    t.string   "title"
    t.string   "url"
    t.datetime "created_at", :null => false
    t.datetime "updated_at", :null => false
  end

  add_index "articles", ["title"], :name => "index_articles_on_title", :unique => true

  create_table "articles_entities", :id => false, :force => true do |t|
    t.integer "article_id"
    t.integer "entity_id"
  end

  add_index "articles_entities", ["article_id", "entity_id"], :name => "index_articles_entities_on_article_id_and_entity_id"

  create_table "clusters", :force => true do |t|
    t.integer  "max_count"
    t.datetime "created_at", :null => false
    t.datetime "updated_at", :null => false
    t.integer  "ttopic_id"
  end

  add_index "clusters", ["ttopic_id"], :name => "index_clusters_on_ttopic_id"

  create_table "entities", :force => true do |t|
    t.string   "name"
    t.integer  "count"
    t.datetime "created_at", :null => false
    t.datetime "updated_at", :null => false
    t.integer  "cluster_id"
  end

  add_index "entities", ["cluster_id"], :name => "index_entities_on_cluster_id"

  create_table "sections", :force => true do |t|
    t.string   "title"
    t.string   "url"
    t.datetime "created_at", :null => false
    t.datetime "updated_at", :null => false
  end

  create_table "sections_ttopics", :id => false, :force => true do |t|
    t.integer "section_id"
    t.integer "ttopic_id"
  end

  add_index "sections_ttopics", ["section_id", "ttopic_id"], :name => "index_sections_ttopics_on_section_id_and_ttopic_id"

  create_table "ttopics", :force => true do |t|
    t.string   "name"
    t.string   "url"
    t.datetime "created_at", :null => false
    t.datetime "updated_at", :null => false
  end

  add_index "ttopics", ["name"], :name => "index_ttopics_on_name", :unique => true

end
