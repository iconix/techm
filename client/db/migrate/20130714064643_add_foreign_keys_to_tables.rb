class AddForeignKeysToTables < ActiveRecord::Migration
  def change
    add_column :clusters, :ttopic_id, :integer
    add_column :entities, :cluster_id, :integer

    add_index :clusters, :ttopic_id
    add_index :entities, :cluster_id
  end
end
