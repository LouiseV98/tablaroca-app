'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const drywallTechniques = [
  {
    title: "Instalación Básica",
    description: "Técnica fundamental para instalar paneles de tablaroca en paredes y techos.",
    image: "/placeholder.svg?height=400&width=600"
  },
  {
    title: "Acabado Liso",
    description: "Proceso para lograr una superficie perfectamente lisa y sin imperfecciones.",
    image: "/placeholder.svg?height=400&width=600"
  },
  {
    title: "Texturizado",
    description: "Aplicación de diferentes texturas decorativas sobre la superficie de la tablaroca.",
    image: "/placeholder.svg?height=400&width=600"
  },
  {
    title: "Esquinas y Bordes",
    description: "Técnicas para lograr esquinas y bordes perfectos en las instalaciones de tablaroca.",
    image: "/placeholder.svg?height=400&width=600"
  }
]

export function DrywallShowcaseComponent() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [designId, setDesignId] = useState<string>(''); // Cambié a design_id
  const [imageUrl, setImageUrl] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [uploadedImages, setUploadedImages] = useState<{ design_id: string, url: string }[]>([]);

  useEffect(() => {
    const fetchImages = async () => { // Añadir console.log para verificar el valor
        try {
          const response = await axios.get(`http://127.0.0.1:5001/images/5`);
          setUploadedImages(response.data);
        } catch (error) {
          console.error('Error fetching images:', error);
        
      } 
    };
  
    fetchImages();
  }, [designId]); // Solo se ejecuta cuando designId cambia
  


  const handleDesignIdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    console.log("Nuevo design_id:", e.target.value);  // Añadir console.log
    setDesignId(e.target.value);
  };

  const handleImageUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setImageUrl(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!designId) {
    setMessage('No se pudo obtener el ID del diseño');
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:5001/images', {
      design_id: designId,
      url: imageUrl
    });

    setMessage('URL de imagen cargada con éxito');
    setImageUrl('');
    setDesignId('');
  } catch (error) {
    setMessage('Error al cargar la URL de la imagen');
    console.error(error);
  }
};

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % drywallTechniques.length)
  }

  const prevSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + drywallTechniques.length) % drywallTechniques.length)
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
        const response = await axios.post(
            'http://127.0.0.1:5000/login', 
            { username, password},
            {
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        );
        if (response.status === 200) {
            setIsLoggedIn(true);
            console.log('Sesión iniciada con éxito:', response.data);
        }
        const token = response.data.token;
        console.log("Token:", token);
    } catch (error: any) {
      if (error.response) {
          console.error('Respuesta del servidor:', error.response.data);
          console.error('Código de estado:', error.response.status);
      } else if (error.request) {
          console.error('No se recibió respuesta del servidor:', error.request);
      } else {
          console.error('Error al configurar la solicitud:', error.message);
      }
  }
};

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await axios.post('http://127.0.0.1:5000/register', { username, password })
      if (response.status === 201) {
        setIsLoggedIn(true)
        console.log('Usuario registrado con éxito:', response.data)
      }
    } catch (error) {
      console.error('Error al registrar usuario:', error)
    }
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setUsername('')
    setPassword('')
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
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
                          placeholder='Usuario' 
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
                          placeholder='Contraseña'
                          required 
                        />
                      </div>
                      <Button type="submit" className="w-full mt-4" onSubmit={handleLogin}>Iniciar Sesión</Button>
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
                          placeholder='Ingrese un nombre de usuario'
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
                          placeholder='Ingrese una contraseña' 
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
        
        
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900">Galería de Técnicas</h2>
          <div className="relative">
            <img
              src={drywallTechniques[currentIndex].image}
              alt={drywallTechniques[currentIndex].title}
              className="w-full h-72 object-cover rounded-lg"
            />
            <div className="absolute top-1/2 left-2 transform -translate-y-1/2">
              <Button variant="ghost" onClick={prevSlide}>
                <ChevronLeft className="w-6 h-6 text-white" />
              </Button>
            </div>
            <div className="absolute top-1/2 right-2 transform -translate-y-1/2">
              <Button variant="ghost" onClick={nextSlide}>
                <ChevronRight className="w-6 h-6 text-white" />
              </Button>
            </div>
          </div>
        </div>

        <div>
          <form onSubmit={handleSubmit}>
            <div>
              <Label htmlFor="designId">ID del Diseño</Label>
              <Input
                id="designId"
                value={designId} // Cambié a design_id
                onChange={handleDesignIdChange}
                required
              />
            </div>
            <div className="mt-2">
              <Label htmlFor="imageUrl">URL de la Imagen</Label>
              <Input
                id="imageUrl"
                value={imageUrl}
                onChange={handleImageUrlChange}
                required
              />
            </div>
            <Button type="submit" className="mt-4">Subir Imagen</Button>
          </form>
          {message && <p className="mt-4">{message}</p>}
        </div>

        <div>
          <h2 className="text-2xl font-bold text-gray-900 mt-12">Imágenes Subidas</h2>
          <div className="grid grid-cols-3 gap-4 mt-4">
            {uploadedImages.map((image) => (
              <div key={image.design_id} className="border p-2 rounded-lg">
                <img
                  src={image.url}
                  alt={`Imagen ${image.design_id}`}
                  className="w-full h-40 object-cover rounded-lg"
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
