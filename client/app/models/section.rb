class Section < ActiveRecord::Base
  attr_accessible :title, :url

  has_and_belongs_to_many :ttopics
  has_many :clusters, through: :ttopics
  has_many :entities, through: :clusters
  has_many :articles, through: :entities

  validates :title, presence: true
  validates :url, presence: true
end
