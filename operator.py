# modal operator...
# have to check this...

class PolyCountOperator(bpy.types.Operator): 
    bl_idname = "view3d.polycount"
    bl_label = "Polygon Count Display Tool"
    bl_description = "Display polygon count in the 3D-view"
  
    _handle = None
    #_timer = None 
    
    all_triangle_count = dict()
    obj_triangle_count = dict() 
    sel_triangle_count = dict()
     
    #show = dict() 
  
    def modal(self, context, event): 
        if context.area: 
            context.area.tag_redraw() 
  
        self.update_polycount(context) 
  
        if not context.window_manager.polycount_run: 
            # stop script 
            view3dId = get_space_id(context.space_data) 
            context.region.callback_remove(self._handle) 
            return {'CANCELLED'} 
  
        return {'PASS_THROUGH'} 
  
    def cancel(self, context): 
        if context.window_manager.polycount_run: 
            context.region.callback_remove(self._handle) 
            context.window_manager.polycount_run = False
        return {'CANCELLED'} 
  
    #@classmethod 
    #def poll(cls, context): 
    #    print("poll") 
    #     
    #    cls.update_polycount(context) 
    #     
    #    return context.active_object is not None 
  
    def update_polycount(self, context): 
        all_tris = 0
        obj_tris = 0
        sel_tris = 0 
  
        for object in context.visible_objects: 
            if (object.type == 'MESH'):
                all_tris += get_triangle_count(object)
  
        for object in context.selected_objects: 
            if (object.type == 'MESH'): 
                obj_tris += get_triangle_count(object) 
                 
        for object in context.selected_objects: 
            if (object.type =='MESH'): 
                sel_tris += get_triangle_count_edit(object) 
                  
        sc = context.scene 
  
        view3dId = get_space_id(context.space_data) 
  
        PolyCountOperator.all_triangle_count[view3dId] = all_tris 
        PolyCountOperator.obj_triangle_count[view3dId] = obj_tris
        PolyCountOperator.sel_triangle_count[view3dId] = sel_tris  
  
    #def execute(self, context): 
    #    print("execute") 
    #    return {'FINISHED'} 
  
    def invoke(self, context, event): 
        #print("invoke") 
  
        if context.area.type == 'VIEW_3D':
            if context.window_manager.polycount_run == False: 
                # operator is called for the first time, start everything 
                print("initialized") 
                context.window_manager.polycount_run = True
                context.window_manager.modal_handler_add(self) 
  
                self._handle = context.region.callback_add(draw_callback_px, 
                    (self, context), 'POST_PIXEL') 
  
                return {'RUNNING_MODAL'} 
            else: 
                # operator is called again, stop displaying 
                context.window_manager.polycount_run = False
                print("stopped") 
                return {'CANCELLED'} 
        else: 
            self.report({'WARNING'}, "View3D not found, can't run operator") 
            return {'CANCELLED'} 