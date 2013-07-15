class Section < ActiveRecord::Base
  attr_accessible :title, :url

  has_many :ttopics
  has_many :clusters, through: :ttopics
  has_many :entities, through: :clusters
  has_many :articles, through: :entities
end
