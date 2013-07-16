class AddIndexToArticlesTitle < ActiveRecord::Migration
  def change
    # to help with populate:gn task
    add_index :articles, :title, unique: true
  end
end
