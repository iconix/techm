require 'json'
require 'set'

namespace :populate do
  desc "Fill database with Google News data"
  task gn: :environment do
  	parsed = JSON.parse(File.read(File.join(File.dirname(__FILE__), '../../../', 'data-layer/output/full_output.json')))
  	
    sections = parsed["SECTIONS"]
    for s in sections
    	section_title = s["title"]
    	section_url = s["url"]

    	section = Section.create!(title: section_title,
                                url: section_url)

      #p section

      ttopics = s["TTOPICS"]
      for tt in ttopics
        ttopic_name = tt["name"]
        ttopic_url = tt["url"]
       
        if not Ttopic.exists?(name: ttopic_name)
          ttopic = Ttopic.create!(name: ttopic_name,
                                  url: ttopic_url)
        else
          ttopic = Ttopic.find_by_name(ttopic_name) # indexed
        end

        section.ttopics << ttopic unless section.ttopics.exists? ttopic
        ttopic.sections << section unless ttopic.sections.exists? section

        clusters = tt["ENTITIES"]
        for c in clusters
          cluster = ttopic.clusters.new

          #p cluster

          max_count = 0
          for e in c
            entity_name = e["name"]
            entity_count = e["count"]

            entity = cluster.entities.new(name: entity_name,
                                              count: entity_count)

            if entity_count > max_count
              max_count = entity_count
            end

            #p entity

            articles = e["ARTICLES"]
            for a in articles
              article_title = a["title"]
              article_url = a["url"]

              if not Article.exists?(title: article_title)
                article = Article.new(title: article_title,
                                          url: article_url)
              else
                article = Article.find_by_title(article_title) # indexed
              end

              entity.articles << article unless entity.articles.exists? article
              article.entities << entity unless article.entities.exists? entity

            end
          end

          cluster.max_count = max_count
          cluster.save
        end
      end
    end
  end
end
