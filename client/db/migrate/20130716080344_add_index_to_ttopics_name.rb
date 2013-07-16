class AddIndexToTtopicsName < ActiveRecord::Migration
  def change
    # to help with populate:gn task
    add_index :ttopics, :name, unique: true
  end
end
