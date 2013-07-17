class Cluster < ActiveRecord::Base
  attr_accessible :max_count

  belongs_to :ttopic
  has_many :entities
  has_many :articles, through: :entities

  validates :max_count, presence: true
end
