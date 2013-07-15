class CreateTtopics < ActiveRecord::Migration
  def change
    create_table :ttopics do |t|
      t.string :name
      t.string :url

      t.timestamps
    end
  end
end
