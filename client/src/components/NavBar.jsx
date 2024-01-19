import ThemeSelector from "./ThemeSelector";

function NavBar() {
  return (
    <>
      <div className="flex justify-center border-b-[5px]">
        <div className="p-4 flex justify-between items-center max-w-screen-lg w-full">
          {/* Logo y Título a la izquierda */}
          <div className="flex items-center">
            {/* <i class="nes-icon close is-medium"></i> */}
            <h1 className="text-2xl font-bold">ChatConnect</h1>
          </div>
          <ThemeSelector />

          {/* Botón a la derecha */}
          <div className="flex gap-2">
            <button class="btn btn-primary">Log in</button>
            <button class="btn btn-secondary btn-outline">Sign up</button>
          </div>
        </div>
      </div>
    </>
  )
}

export default NavBar;