module default {
    type Perfume {
        required property name -> str;
        property rating -> float64;
        property best_rating -> int64;
        property rating_count -> int64;
        property description -> str;
	    link owned_by -> Brand;
        multi link belongs_to -> ScentGroup;
	    multi link contains -> Notes;
	    multi link has_review := .<user_of[is Review];
	    constraint exclusive on ((.name, .owned_by));
    }

    type Brand {
        required property name -> str;
	    multi link has_perfumes := .<owned_by[is Perfume];
	    constraint exclusive on (.name);
    }

    type ScentGroup {
        required property name -> str;
        multi link has_perfumes := .<belongs_to[is Perfume];
	    constraint exclusive on (.name);
    }

    type Notes {
        required property name -> str;
        multi link has_perfumes := .<contains[is Perfume];
	    constraint exclusive on ((.name));
    }

    type Review {
        property content -> str;
        multi link user_of -> Perfume;
    }
}