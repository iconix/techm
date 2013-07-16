class CreateRefSections < ActiveRecord::Migration
  def change
    create_table :ref_sections do |t|
      t.integer :ttopic_id

      t.timestamps
    end

    add_column :sections, :ref_section_id, :integer
  end
end
