'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { ChevronLeft, ChevronRight, User, Lock, Mail} from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const drywallTechniques = [
  {
    title: "Instalación Básica",
    description: "Técnica fundamental para instalar paneles de tablaroca en paredes y techos.",
    image: "/images/1.jpg"
  },
  {
    title: "Acabado Liso",
    description: "Proceso para lograr una superficie perfectamente lisa y sin imperfecciones.",
    image: "/images/2.jpg"
  },
  {
    title: "Texturizado",
    description: "Aplicación de diferentes texturas decorativas sobre la superficie de la tablaroca.",
    image: "/images/3.jpg"
  },
  {
    title: "Esquinas y Bordes",
    description: "Técnicas para lograr esquinas y bordes perfectos en las instalaciones de tablaroca.",
    image: "/images/4.jpg"
  }
]

export function DrywallShowcaseComponent() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [designId, setDesignId] = useState('')
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [uploadedImages, setUploadedImages] = useState<string[]>([]);

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % drywallTechniques.length)
  }

  const prevSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + drywallTechniques.length) % drywallTechniques.length)
  }

  const fetchImages = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5001/images');
      setUploadedImages(response.data);
    } catch (error) {
      console.error('Error fetching images:', error);
    }
  };

  useEffect(() => {
    fetchImages();
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await axios.post('http://127.0.0.1:5000/login', { username, password })
      if (response.status === 200) {
        setIsLoggedIn(true)
      }
    } catch (error) {
      console.error(error)
    }
  }

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await axios.post('http://127.0.0.1:5000/register', { username, password })
      if (response.status === 201) {
        setIsLoggedIn(true)
      }
    } catch (error) {
      console.error(error)
    }
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setUsername('')
    setPassword('')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!designId || !imageFile) {
      console.error('Error: Todos los campos son obligatorios.')
      return
    }
    const formData = new FormData()
    formData.append('design_id', designId)
    formData.append('image', imageFile)

    try {
      await axios.post('http://127.0.0.1:5001/images/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setImageFile(null)
      setDesignId('')
    } catch (error) {
      console.error('Error al subir la imagen:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Encabezado y sección de autenticación */}
        <div className="flex justify-between items-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900">Instalación en Tablaroca</h1>
          {isLoggedIn ? (
            <Button onClick={handleLogout}>Cerrar Sesión</Button>
          ) : (
            <Tabs defaultValue="login" className="w-[400px]">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="login">Iniciar Sesión</TabsTrigger>
                <TabsTrigger value="register">Registrarse</TabsTrigger>
              </TabsList>
              <TabsContent value="login">
                <Card>
                  <CardHeader>
                    <CardTitle>Iniciar Sesión</CardTitle>
                    <CardDescription>Ingresa tus credenciales para acceder a tu cuenta.</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <form onSubmit={handleLogin}>
                      <div className="space-y-1">
                        <Label htmlFor="username">Nombre de Usuario</Label>
                        <Input
                          id="username"
                          type="text"
                          value={username}
                          onChange={(e) => setUsername(e.target.value)}
                          placeholder="Usuario"
                          required
                        />
                      </div>
                      <div className="space-y-1">
                        <Label htmlFor="password">Contraseña</Label>
                        <Input
                          id="password"
                          type="password"
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          placeholder="Contraseña"
                          required
                        />
                      </div>
                      <Button type="submit" className="w-full mt-4">Iniciar Sesión</Button>
                    </form>
                  </CardContent>
                </Card>
              </TabsContent>
              <TabsContent value="register">
                <Card>
                  <CardHeader>
                    <CardTitle>Registrarse</CardTitle>
                    <CardDescription>Crea una nueva cuenta para acceder a nuestros servicios.</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <form onSubmit={handleRegister}>
                      <div className="space-y-1">
                        <Label htmlFor="username">Nombre de Usuario</Label>
                        <Input
                          id="username"
                          type="text"
                          value={username}
                          onChange={(e) => setUsername(e.target.value)}
                          placeholder="Ingrese un nombre de usuario"
                          required
                        />
                      </div>
                      <div className="space-y-1">
                        <Label htmlFor="password">Contraseña</Label>
                        <Input
                          id="password"
                          type="password"
                          value={password}
                          onChange={(e) => setPassword(e.target.value)}
                          placeholder="Ingrese una contraseña"
                          required
                        />
                      </div>
                      <Button type="submit" className="w-full mt-4">Registrarse</Button>
                    </form>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          )}
        </div>
        
        {/* Carrousel */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Card className="col-span-1 md:col-span-2">
            <CardHeader>
              <CardTitle>{drywallTechniques[currentIndex].title}</CardTitle>
              <CardDescription>{drywallTechniques[currentIndex].description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="relative">
                <img 
                  src={drywallTechniques[currentIndex].image} 
                  alt={drywallTechniques[currentIndex].title}
                  className="w-full h-100 object-cover rounded-lg"
                />
                <Button 
                  variant="outline" 
                  size="icon" 
                  className="absolute top-1/2 left-4 transform -translate-y-1/2"
                  onClick={prevSlide}
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <Button 
                  variant="outline" 
                  size="icon" 
                  className="absolute top-1/2 right-4 transform -translate-y-1/2"
                  onClick={nextSlide}
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>

        {/* Galería de Técnicas */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Galería de Técnicas</h2>
          <div className="relative">
            <img
              src={drywallTechniques[currentIndex].image}
              alt={drywallTechniques[currentIndex].title}
              className="w-full h-82 object-cover rounded-lg"
            />
            <div className="absolute top-1/2 left-2 transform -translate-y-1/2">
              <Button variant="ghost" onClick={() => setCurrentIndex((prevIndex) => (prevIndex - 1 + drywallTechniques.length) % drywallTechniques.length)}>
                <ChevronLeft className="w-6 h-6 text-white" />
              </Button>
            </div>
            <div className="absolute top-1/2 right-2 transform -translate-y-1/2">
              <Button variant="ghost" onClick={() => setCurrentIndex((prevIndex) => (prevIndex + 1) % drywallTechniques.length)}>
                <ChevronRight className="w-6 h-6 text-white" />
              </Button>
            </div>
          </div>
        </div>

        {/* Formulario para subir imágenes */}
        <div>
          <form onSubmit={handleSubmit}>
            <div>
              <Label htmlFor="designId">ID del Diseño</Label>
              <Input
                id="designId"
                value={designId}
                onChange={(e) => setDesignId(e.target.value)}
                required
              />
            </div>
            <div className="mt-2">
              <Label htmlFor="image">Seleccionar Imagen</Label>
              <Input
                id="image"
                type="file"
                accept="image/*"
                onChange={(e) => setImageFile(e.target.files ? e.target.files[0] : null)}
                required
              />
            </div>
            <Button type="submit" className="mt-4">Subir Imagen</Button>
          </form>
        </div>

        {/* Imágenes Subidas */}
        <div>
  <h2 className="text-2xl font-bold text-gray-900">Imágenes Subidas</h2>
  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
    {uploadedImages.length > 0 ? (
      uploadedImages.map((image, index) => (
        <div key={index} className="relative">
          <img
            src={`http://127.0.0.1:5001/uploads/${image}`}
            alt={`Imagen ${index + 1}`}
            className="w-full h-auto object-cover rounded-lg"
          />
        </div>
      ))
    ) : (
      <p>No hay imágenes disponibles.</p>
    )}
  </div>
</div>
      </div>
    </div>
    </div>
  )
}
