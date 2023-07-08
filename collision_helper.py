from constantes import *

class CollisionHelper():
    @staticmethod
    def are_colliding(rect_one, rect_two):
        return rect_one.colliderect(rect_two)
    
    @staticmethod
    def player_colliding_with_entity(player, entity):
        return CollisionHelper.entities_colliding(player, entity)
    
    @staticmethod
    def entities_colliding(first_entity, second_entity):
        return CollisionHelper.are_colliding(first_entity.collition_rect, second_entity.collition_rect)

    @staticmethod
    def fallable_will_collide_with_entity(fallable, entity):
        return CollisionHelper.fallable_will_collide_with_rect(fallable, entity.ground_collition_rect)
    
    @staticmethod
    def fallable_colliding_with_entity(fallable, entity):
        return CollisionHelper.fallable_colliding_with_rect(fallable, entity.ground_collition_rect)
    
    @staticmethod
    def fallable_will_collide_with_rect(fallable, rect):
        fallable_x = fallable.ground_collition_rect.x
        fallable_y = fallable.ground_collition_rect.bottom
        fallable_next_y = fallable_y + fallable.velocity_y
        will_collide = False

        if fallable_x > rect.left and fallable_x < rect.right:
            print(f"inside platform - is-above: {fallable_y < rect.top} - will-be-below: {fallable_next_y >= rect.top}")
            will_collide = fallable_y < rect.top and fallable_next_y >= rect.top


        return will_collide
    
    @staticmethod
    def fallable_colliding_with_rect(fallable, rect):
        return CollisionHelper.are_colliding(fallable.ground_collition_rect, rect)
    
    @staticmethod
    def entity_will_collide_with_ground(player):
        
        player_y = player.ground_collition_rect.y
        player_next_y = player_y + player.velocity_y
        
        will_collide = player_y < GROUND_LEVEL and player_next_y >= GROUND_LEVEL

        return will_collide
    
    @staticmethod
    def entity_is_grounded(entity, level):
        return CollisionHelper.are_colliding(entity.ground_collition_rect, level.ground)
    
    @staticmethod
    def is_against_edge(entity):
        return CollisionHelper.is_against_left_edge(entity) or CollisionHelper.is_against_right_edge(entity)

    @staticmethod
    def is_against_left_edge(entity):
        return entity.rect.left <= 0
    
    @staticmethod
    def is_against_right_edge(entity):
        return entity.rect.right >= ANCHO_VENTANA

    @staticmethod
    def consumable_must_float(consumable, ground):
        return ground.top - consumable.rect.y < consumable.float_height

                
    
