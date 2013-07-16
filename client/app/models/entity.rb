class Entity < ActiveRecord::Base
  attr_accessible :count, :name

  belongs_to :cluster
  has_and_belongs_to_many :articles

  validates :count, presence: true
  validates :name, presence: true
end
