import bpy

bl_info = {
    "name": "Batch Render",
    "author": "Andrea Calzavacca",
    "version": (0, 1, 1),
    "blender": (2, 7, 8),
    "location": "Render > Batch Render",
    "description": "Make possible to render more than one camera without manually start every render",
    "warning": "",
    "category": "Render"}

def get_cameras():
    """Retrieve all cameras' names for the current scene"""
    l = []
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            l.append(obj)
    return l

class CamProp(bpy.types.PropertyGroup):
    
    @classmethod
    def register(cls):
        
        bpy.types.Object.custom = bpy.props.PointerProperty(
            name="Custom properties",
            description="Custom Properties for Cameras",
            type=cls,
            )
            
        cls.isSelected = bpy.props.BoolProperty(
            description="True if Camera is selected to be used",
            default=False
            )
            
    @classmethod
    def unregister(cls):
        del bpy.types.Object.custom

class BatchRender(bpy.types.Operator):
    """Batch Render"""
    bl_idname = "render.batch"
    bl_label = "Subsequently render all selected cameras"
    bl_options = {'REGISTER', 'UNDO'}

    # Define some variables to register
    _timer = None
    cam = get_cameras()
    shots = []
    stop = None
    rendering = None
    path = "//"

    # Define the handler functions. I use pre and
    # post to know if Blender "is rendering"
    def pre(self, dummy):
        self.rendering = True

    def post(self, dummy):
        self.shots.pop(0) # This is just to render the next
                          # image in another path
        self.rendering = False

    def cancelled(self, dummy):
        self.stop = True

    def execute(self, context):
        # Define the variables during execution. This allows
        # to define when called from a button
        self.stop = False
        self.rendering = False
        
        for item in self.cam:
            if item.custom.isSelected:
                self.shots.append(item)       

        bpy.context.scene.render.filepath = self.path

        bpy.app.handlers.render_pre.append(self.pre)
        bpy.app.handlers.render_post.append(self.post)
        bpy.app.handlers.render_cancel.append(self.cancelled)

        # The timer gets created and the modal handler
        # is added to the window manager
        self._timer = context.window_manager.event_timer_add(0.5, context.window)
        context.window_manager.modal_handler_add(self)

        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type == 'TIMER': # This event is signaled every half a second
                                  # and will start the render if available

            # If cancelled or no more shots to render, finish.
            if True in (not self.shots, self.stop is True): 

                # We remove the handlers and the modal timer to clean everything
                bpy.app.handlers.render_pre.remove(self.pre)
                bpy.app.handlers.render_post.remove(self.post)
                bpy.app.handlers.render_cancel.remove(self.cancelled)
                context.window_manager.event_timer_remove(self._timer)

                return {"FINISHED"}

            elif self.rendering is False: # Nothing is currently rendering.
                                          # Proceed to render.

                sceneKey = bpy.data.scenes.keys()[0]

                bpy.data.scenes[sceneKey].camera = self.shots[0]
                bpy.data.scenes[sceneKey].render.filepath = self.path + self.shots[0].name
                bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)

        return {"PASS_THROUGH"}
        # This is very important! If we used "RUNNING_MODAL", this new modal function
        # would prevent the use of the X button to cancel rendering, because this
        # button is managed by the modal function of the render operator,
        # not this new operator!

class BatchRenderPanel(bpy.types.Panel):
    bl_idname = "PROPERTIES_PT_batch"
    bl_label = "Batch Render"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}
    
    @classmethod
    def pool(cls, context):
        return context.object is not None
    
    def draw(self, context):
        layout = self.layout
                
        split = layout.split()
        col = split.column()
        
        elements = get_cameras()
        
        i = 0
        for item in elements:
            if i < len(elements)/2:
                col.prop(item.custom, "isSelected", text=item.name)
            elif i == len(elements)/2 or i == (len(elements)+1)/2:
                col = split.column()
                col.prop(item.custom, "isSelected", text=item.name)
            else:
                col.prop(item.custom, "isSelected", text=item.name)
            i += 1
            
        row = layout.row(align=True)
        row.operator("render.batch", text="Batch Render", icon='RENDER_STILL')

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

# START DEBUG SECTION ---------------------------------------------------------------------------------------
# launch addon as script into blender text editor -----------------------------------------------------------

if __name__ == "__main__":
    register()