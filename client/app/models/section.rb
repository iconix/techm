class Section < ActiveRecord::Base
  attr_accessible :title, :url

  has_many :ttopics
  has_many :clusters, through: :ttopics
  has_many :entities, through: :clusters
  has_many :articles, through: :entities

  belongs_to :ref_section

  validates :title, presence: true
  validates :url, presence: true
end
