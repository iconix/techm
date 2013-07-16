class Entity < ActiveRecord::Base
  attr_accessible :count, :name

  belongs_to :cluster
  has_many :articles

  belongs_to :ref_entity

  validates :count, presence: true
  validates :name, presence: true
end
