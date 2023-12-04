CREATE MIGRATION m14zbetimchghp2ugy4e4wiuatnku4nmczhj3hz5cxsukzfqfffmwa
    ONTO initial
{
  CREATE TYPE default::Brand {
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE CONSTRAINT std::exclusive ON (.name);
  };
  CREATE TYPE default::Perfume {
      CREATE LINK owned_by: default::Brand;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE CONSTRAINT std::exclusive ON ((.name, .owned_by));
      CREATE PROPERTY best_rating: std::int64;
      CREATE PROPERTY description: std::str;
      CREATE PROPERTY rating: std::float64;
      CREATE PROPERTY rating_count: std::int64;
  };
  ALTER TYPE default::Brand {
      CREATE MULTI LINK has_perfumes := (.<owned_by[IS default::Perfume]);
  };
  CREATE TYPE default::Notes {
      CREATE REQUIRED PROPERTY name: std::str;
  };
  CREATE TYPE default::ScentGroup {
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE CONSTRAINT std::exclusive ON (.name);
  };
  ALTER TYPE default::Notes {
      CREATE LINK belongs_to: default::ScentGroup;
      CREATE CONSTRAINT std::exclusive ON ((.name, .belongs_to));
  };
  ALTER TYPE default::ScentGroup {
      CREATE MULTI LINK has_notes := (.<belongs_to[IS default::Notes]);
  };
  ALTER TYPE default::Perfume {
      CREATE MULTI LINK contains: default::Notes;
      CREATE MULTI LINK belongs_to: default::ScentGroup;
  };
  ALTER TYPE default::Notes {
      CREATE MULTI LINK has_perfumes := (.<contains[IS default::Perfume]);
  };
  ALTER TYPE default::ScentGroup {
      CREATE MULTI LINK has_perfumes := (.<belongs_to[IS default::Perfume]);
  };
  CREATE TYPE default::Review {
      CREATE MULTI LINK user_of: default::Perfume;
      CREATE PROPERTY content: std::str;
      CREATE CONSTRAINT std::exclusive ON (.content);
  };
  ALTER TYPE default::Perfume {
      CREATE MULTI LINK has_review := (.<user_of[IS default::Review]);
  };
};
