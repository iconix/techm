class CreateSectionsTtopics < ActiveRecord::Migration
  def change
    create_table :sections_ttopics, :id => false do |t|
      t.integer :section_id
      t.integer :ttopic_id
    end

    add_index :sections_ttopics, [:section_id, :ttopic_id]
  end
end
