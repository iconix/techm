class CreateRefEntities < ActiveRecord::Migration
  def change
    create_table :ref_entities do |t|
      t.integer :article_id

      t.timestamps
    end

    add_column :entities, :ref_entity_id, :integer
  end
end
