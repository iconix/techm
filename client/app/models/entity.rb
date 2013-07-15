class Entity < ActiveRecord::Base
  attr_accessible :count, :name

  belongs_to :cluster
  has_many :articles
end
