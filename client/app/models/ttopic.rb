class Ttopic < ActiveRecord::Base
  attr_accessible :name, :url

  belongs_to :section
  has_many :clusters
  has_many :entities, through: :clusters
  has_many :articles, through: :entities
end
