class Cluster < ActiveRecord::Base
  belongs_to :ttopic
  has_many :entities
  has_many :articles, through: :entities
end
