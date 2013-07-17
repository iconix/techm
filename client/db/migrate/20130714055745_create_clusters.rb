class CreateClusters < ActiveRecord::Migration
  def change
    create_table :clusters do |t|
      t.integer :max_count

      t.timestamps
    end
  end
end
