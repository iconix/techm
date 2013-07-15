class AddForeignKeysToTables < ActiveRecord::Migration
  def change
    add_column :ttopics, :section_id, :integer
    add_column :clusters, :ttopic_id, :integer
    add_column :entities, :cluster_id, :integer
    add_column :articles, :entity_id, :integer
  end
end
