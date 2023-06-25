class CollisionHelper():
    @staticmethod
    def are_colliding(rect_one, rect_two):
        return rect_one.colliderect(rect_two)
    
    @staticmethod
    def player_colliding_with_entity(player, entity):
        return CollisionHelper.are_colliding(player.collition_rect, entity.collition_rect)

