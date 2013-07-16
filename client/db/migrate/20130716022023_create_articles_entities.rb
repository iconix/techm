class CreateArticlesEntities < ActiveRecord::Migration
  def change
    create_table :articles_entities, :id => false do |t|
      t.integer :article_id
      t.integer :entity_id
    end

    add_index :articles_entities, [:article_id, :entity_id]
  end
end
